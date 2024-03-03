import os
import unittest

from configuration import ConfigurationException
from device.telegram import Telegram
from tests.mock_requestwrapper import MockRequestWrapper
from utils.requests_wrapper import RequestException


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
        t._request = MockRequestWrapper()
        t.setup()
        self.assertEqual("https://api.telegram.org/botfoobar", t._url)
        self.assertEqual([{"action": "http_get_text", "url": 'https://api.telegram.org/', "parameters": None}],
                         t._request._actions)

    def test_send(self):
        t = Telegram({Telegram.CONFIG_TOKEN: 'foobar',
                      Telegram.CONFIG_CHANNEL_ID: 'foobar2',
                      Telegram.CONFIG_BASE_URL: 'https://api.telegram.org'})
        t._request = MockRequestWrapper()
        t.setup()
        t.send_text("testing text")
        self.assertEqual([{'action': 'http_get_text', 'parameters': None,
                           'url': 'https://api.telegram.org/'},
                          {"action": "_post", "url": t._url + "/sendMessage",
                           "data": {'chat_id': 'foobar2', 'text': "testing text"}, "files": None}],
                         t._request._actions)
        t._request._actions = []
        t.send_photo(filename="../resources/aanbellen.jpeg", caption="Testing Caption")
        with open("../resources/aanbellen.jpeg", 'rb') as fh:
            self.assertEqual([
                              {"action": "_post", "url": t._url + "/sendPhoto",
                               "data": {'chat_id': 'foobar2', 'caption': "Testing Caption"},
                               "files": {'photo': fh.name}}],
                             t._request._actions)
        t._request._actions = []
        self.assertRaises(RequestException, t.send_photo, filename="../resources/aanbellen.jpeg", caption="Exception")


