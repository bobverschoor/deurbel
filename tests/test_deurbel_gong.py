import unittest

from configuration import ConfigurationException
from deurbel_gong import DeurbelGong
from gateway.gpio_gateway import RaspberryPiException


class TestDeurbelGong(unittest.TestCase):
    def test_setup(self):
        self.assertRaises(ConfigurationException, DeurbelGong,
                          {'enabled': True, 'output': True, 'gong_duration_ms': 100000, 'gpio_channel': 7})

        self.assertRaises(RaspberryPiException, DeurbelGong,
                          {'enabled': True, 'output': True, 'gong_duration_ms': 10000, 'gpio_channel': 100})

    def test_sound(self):
        gong = DeurbelGong({'enabled': True, 'output': True, 'gong_duration_ms': 1, 'gpio_channel': 7})
        gong._pi._gpio.actions = []
        gong.sound()
        self.assertEqual([{'output': {'pin': 7, 'value': 1}}, {'output': {'pin': 7, 'value': 0}}],
                         gong._pi._gpio.actions)

    def test_sound_disabled(self):
        gong = DeurbelGong({'enabled': False, 'output': True, 'gong_duration_ms': 1, 'gpio_channel': 7})
        gong._pi._gpio.actions = []
        gong.sound()
        gong.silence()
        self.assertEqual([], gong._pi._gpio.actions)
