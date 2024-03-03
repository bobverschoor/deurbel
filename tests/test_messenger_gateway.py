import unittest

from configuration import Configuration
from device.telegram import Telegram
from gateway.messenger_gateway import MessengerGateway
from tests.mock_requestwrapper import MockRequestWrapper
from tests.mock_telegram import MockTelegram


class TestMessengerGateway(unittest.TestCase):
    def test_setup(self):
        mg = MessengerGateway({})
        self.assertFalse(mg.enabled)
        mg = MessengerGateway({Configuration.ENABLED: True})
        mg.setup()
        self.assertFalse(mg.enabled)
        mg = MessengerGateway({Configuration.ENABLED: True, mg.DEVICES: []})
        mg.setup()
        self.assertFalse(mg.enabled)
        mg = MessengerGateway({Configuration.ENABLED: True, mg.DEVICES: [{}]})
        mg.setup()
        self.assertFalse(mg.enabled)
        mg = MessengerGateway({Configuration.ENABLED: True, mg.DEVICES: [{mg.NAME: "televisie"}]})
        mg.setup()
        self.assertFalse(mg.enabled)
        mg = MessengerGateway({Configuration.ENABLED: True,
                               MessengerGateway.DEVICES: [{MessengerGateway.NAME: "telegram",
                                                           Telegram.CONFIG_TOKEN: 'foobar',
                                                           Telegram.CONFIG_CHANNEL_ID: 'foobar2',
                                                           Telegram.CONFIG_BASE_URL: 'https://api.telegram.org'}]})
        mg._devices[0]._request = MockRequestWrapper()
        mg.setup()
        self.assertTrue(mg.enabled)
        self.assertEqual(1, len(mg._devices))

    def test_send(self):
        mg = MessengerGateway({Configuration.ENABLED: True,
                               MessengerGateway.DEVICES: [{MessengerGateway.NAME: "telegram"}]})
        mock_telegram = MockTelegram()
        mg._devices = [mock_telegram]
        mg.send(text="test")
        mg.send(photo_filename="deurbel.log", text="test2")
        mg.send(photo_filename="onvindbaar.jpg", text="test3")
        self.assertEqual([{"method": "send_text", "text": "test"},
                          {"method": "send_photo", "filename": "deurbel.log", "caption": "test2"},
                          {"method": "send_text", "text": "test3"}],
                         mock_telegram._action)
