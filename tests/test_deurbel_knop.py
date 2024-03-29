import unittest

from configuration import ConfigurationException
from device.deurbel_knop import DeurbelKnop
from gateway.gpio_gateway import RaspberryPiException


class TestDeurbelKnop(unittest.TestCase):
    def test_setup(self):
        self.assertRaises(ConfigurationException, DeurbelKnop,
                          {'enabled': True, 'output': True, 'bounce_time_ms': 1001, 'gpio_channel': 8}, None)
        self.assertRaises(ConfigurationException, DeurbelKnop,
                  {'enabled': False, 'output': True, 'bounce_time_ms': 1000, 'gpio_channel': 8}, None)

        self.assertRaises(RaspberryPiException, DeurbelKnop,
                          {'enabled': True, 'output': True, 'bounce_time_ms': 500, 'gpio_channel': 100,
                           'edge_detection': 0, 'resistor': 0}, None)

    def test_pressed_wrong_channel(self):
        knop = DeurbelKnop({'enabled': True, 'output': True, 'bounce_time_ms': 1, 'gpio_channel': 7,
                    'edge_detection': 'rising', 'resistor': 'pull_up'},
                   None)
        self.assertFalse(knop.pressed(8))

    def test_using_mock(self):
        knop = DeurbelKnop({'enabled': True, 'output': True, 'bounce_time_ms': 1, 'gpio_channel': 7,
                            'edge_detection': 'rising', 'resistor': 'pull_up'},
                           None)
        knop._pi._gpio.actions = []
        self.assertTrue(knop.using_mock())
        knop._pi._gpio.VERSION = "3.11"
        self.assertFalse(knop.using_mock())
