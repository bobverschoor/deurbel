import unittest

from configuration import ConfigurationException
from device.telegram import Telegram


class TestTelegram(unittest.TestCase):
    def test_setup(self):
        t = Telegram({})
        self.assertRaises(ConfigurationException, t.setup)
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar'})
        self.assertRaises(ConfigurationException, t.setup)
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar', Telegram.CONFIG_CHANNEL_ID: 'foobar2'})
        self.assertRaises(ConfigurationException, t.setup)
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar', Telegram.CONFIG_CHANNEL_ID: 'foobar2',
                      Telegram.CONFIG_BASE_URL: 'htt://api.telegram.org'})
        self.assertRaises(ConfigurationException, t.setup)
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar', Telegram.CONFIG_CHANNEL_ID: 'foobar2',
                      Telegram.CONFIG_BASE_URL: 'https://api.telegram.og'})
        self.assertRaises(ConfigurationException, t.setup)
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar',
                      Telegram.CONFIG_CHANNEL_ID: 'foobar2',
                      Telegram.CONFIG_BASE_URL: 'https://api.telegram.org'})
        t.setup()
        self.assertEqual("https://api.telegram.org/botfoobar", t._url)


if __name__ == '__main__':
    unittest.main()
