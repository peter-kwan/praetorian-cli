import time
from urllib.parse import urlparse

import pytest
import requests

from praetorian_cli.handlers.utils import Asset
from praetorian_cli.sdk.test import BaseTest


@pytest.mark.coherence
class TestAssetWebhook(BaseTest):
    asset_payload = dict(dns=f"contoso-{time.time()}.com", name="10.1.1.5")
    webhook = ""

    def setup_class(self):
        self.chariot, self.username = BaseTest.setup_chariot(self)

    def test_create_webhook(self):
        if self.chariot.get_webhook():
            self.chariot.delete_webhook()
        TestAssetWebhook.webhook = self.chariot.add_webhook()
        parsed_url = urlparse(self.webhook)
        assert all([parsed_url.scheme, parsed_url.netloc]), "Response is not a valid URL"

    def test_add_asset(self):
        print(TestAssetWebhook.webhook)
        webhook_response = requests.post(url=TestAssetWebhook.webhook, json=self.asset_payload)
        assert webhook_response.status_code == 200, "Webhook POST request failed"

    def test_my_asset(self):
        response = self.chariot.my(dict(key=f'#asset#'))
        assert any(my_asset['dns'] == self.asset_payload['dns'] for my_asset in response['assets']), \
            "None of the assets matched self.asset_payload['dns']"

    def test_update_asset(self):
        response = self.chariot.update('asset',
                                       dict(key=f'#asset#{self.asset_payload["dns"]}#{self.asset_payload["name"]}',
                                            status=Asset.FROZEN.value))[0]
        assert response['status'] == Asset.FROZEN.value, "Response does not have correct status"
        assert response['dns'] == self.asset_payload['dns']
