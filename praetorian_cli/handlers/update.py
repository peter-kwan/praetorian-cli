import click

from praetorian_cli.handlers.chariot import chariot
from praetorian_cli.handlers.utils import Status
from praetorian_cli.handlers.cli_decorators import cli_handler, status_options


@chariot.group()
@cli_handler
def update(ctx):
    """Update a resource in Chariot"""
    pass


def create_update_command(item_type, status_choices):
    @update.command(item_type, help=f"Update {item_type} using object key")
    @click.argument('key', required=True)
    @status_options(status_choices)
    def command(controller, key, status, comment):
        controller.update(item_type, dict(key=key, status=status, comment=comment))


create_update_command('asset', Status['asset'])
create_update_command('risk', Status['risk'])
create_update_command('job', Status['job'])
