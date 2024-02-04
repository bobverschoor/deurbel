

import requests
from requests.exceptions import InvalidSchema, ConnectionError

from configuration import ConfigurationException


class Telegram:
    CONFIG_TOKEN = 'token'
    CONFIG_CHANNEL_ID = 'channel_id'
    CONFIG_BASE_URL = 'base_url'

    def __init__(self, config):
        self._config = config
        self._url = ""
        self._channel_id = ""

    def setup(self):
        try:
            token = self._config[self.CONFIG_TOKEN]
            if not token.startswith('bot'):
                token = "bot" + token
            self._channel_id = self._config[self.CONFIG_CHANNEL_ID]
            base_url = self._config[self.CONFIG_BASE_URL]
            if not base_url.endswith("/"):
                base_url = base_url + "/"
            r = requests.get(base_url)
            self._url = base_url + token
        except KeyError as e:
            raise ConfigurationException(e)
        except InvalidSchema as e:
            raise ConfigurationException(e)
        except ConnectionError as e:
            raise ConfigurationException(e)

    def send(self):
        method = "/sendMessage"
        url = self._url + method
