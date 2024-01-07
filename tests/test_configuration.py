import unittest

from configuration import Configuration, ConfigurationException


class TestConfiguration(unittest.TestCase):

    def test_configuration_init(self):
        self.assertRaises(ConfigurationException, Configuration, "tests/Fake.toml")

    def test_get_active_modules(self):
        config = Configuration("test-config.toml")
        active_modules = config.get_active_module_names()
        self.assertEqual(2, len(active_modules))

    def test_get_module(self):
        config = Configuration("test-config.toml")
        self.assertEqual({"enabled": False, "input": True}, config.get_module("photo"))
