import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.cli_decorators import cli_handler
from praetorian_cli.handlers.utils import AssetPriorities, AddRisk


@chariot.group()
@cli_handler
def add(ctx):
    """ Add a resource to Chariot """
    pass


@add.command('asset')
@click.option('-name', '--name', required=True, help='The name of the asset, e.g, IP address, GitHub repo URL')
@click.option('-dns', '--dns', required=False, help='The DNS of the asset')
@click.option('--priority', type=click.Choice(AssetPriorities.keys()),
              default='standard', help='The priority of the asset. Default: standard')
@cli_handler
def asset(controller, name, dns, priority):
    """ Add an asset """
    if dns is None:
        dns = name
    controller.add('asset', dict(name=name, dns=dns, status=AssetPriorities[priority]))


@add.command('file')
@click.argument('name')
@cli_handler
def upload(controller, name):
    """ Upload a file """
    controller.upload(name, "manual")


@add.command('definition')
@click.argument('path')
@click.option('-name', '--name', required=False, help='The risk name definition. Default: the filename used')
@cli_handler
def definition(controller, path, name):
    """ Upload a definition to use for a risk """
    if name is None:
        name = path.split('/')[-1]
    controller.upload(path, "definition", f"definitions/{name}")


@add.command('webhook')
@cli_handler
def webhook(controller):
    """ Add an authenticated URL for posting assets and risks """
    response = controller.add_webhook()
    print(response)


@add.command('risk')
@click.argument('name', required=True)
@click.option('-asset', '--asset', required=True, help='Key of an existing asset')
@click.option('-class', '--class', 'clss', default='weakness',
              type=click.Choice(['weakness', 'exposure', 'misconfiguration']),
              help='Class of the risk. Default is weakness')
@click.option('-status', '--status', type=click.Choice([s.value for s in AddRisk]), required=True,
              help=f'Status of the risk')
@click.option('-comment', '--comment', default='', help='Comment for the risk')
@cli_handler
def risk(controller, name, asset, clss, status, comment):
    """
    Add a risk

    NAME is the name of the risk
    """
    controller.add('risk', {'key': asset, 'name': name, 'status': status, 'comment': comment, 'class': clss})


@add.command('job')
@cli_handler
@click.argument('capability', required=True)
@click.option('-asset', '--asset', required=True, help='Key of an existing asset')
def job(controller, capability, asset):
    """ Add a job for an asset """
    controller.add('job', dict(key=asset, name=capability))


@add.command('attribute')
@cli_handler
@click.argument('name', required=True)
@click.option('-key', '--key', required=True, help='Key of an existing asset or risk')
@click.option('-class', '--class', 'clss', required=True, help='Class of the attribute')
def attribute(controller, name, key, clss):
    """ Add an attribute for an asset or risk"""
    params = {
        'key': key,
        'name': name,
        'class': clss
    }
    print(controller.add('attribute', params))
