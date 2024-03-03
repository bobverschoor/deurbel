import unittest

from configuration import Configuration
from device.esp32cam import Esp32Cam
from gateway.photo_gateway import PhotoGateway
from tests.mock_requestwrapper import MockRequestWrapper


class TestPhotoGateway(unittest.TestCase):
    def test_init(self):
        pg = PhotoGateway({})
        self.assertFalse(pg.enabled)
        pg = PhotoGateway({Configuration.ENABLED: True})
        self.assertFalse(pg.enabled)
        pg = PhotoGateway({Configuration.ENABLED: True, pg.DEVICES: []})
        self.assertFalse(pg.enabled)
        pg = PhotoGateway({Configuration.ENABLED: True, pg.DEVICES: [{}]})
        self.assertFalse(pg.enabled)
        pg = PhotoGateway({Configuration.ENABLED: True, pg.DEVICES: [{pg.NAME: "televisie"}]})
        self.assertFalse(pg.enabled)
        pg = PhotoGateway({Configuration.ENABLED: True, Configuration.TEMP_DIR: '/tmp',
                           PhotoGateway.DEVICES: [{PhotoGateway.NAME: "esp32cam",
                                                   Esp32Cam.CONFIG_URL: 'https://httpbin.org',
                                                   Esp32Cam.CONFIG_CAPTURE_PATH: 'cap',
                                                   Esp32Cam.CONFIG_CONTROL_PATH: 'con',
                                                   Esp32Cam.CONFIG_STATUS_PATH: 'status/200',
                                                   Esp32Cam.CONFIG_CONTROL_PARAMETERS: {}}]})
        pg._devices[0]._request = MockRequestWrapper()
        pg.setup()
        self.assertTrue(pg.enabled)
        self.assertEqual(1, len(pg._devices))
        self.assertEqual([{'action': 'http_get_json', 'parameters': None,
                           'url': 'https://httpbin.org/status/200'}], pg._devices[0]._request._actions)
