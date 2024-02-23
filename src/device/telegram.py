import logging

import requests
from requests.exceptions import InvalidSchema, ConnectionError, MissingSchema

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
            requests.get(base_url)
            self._url = base_url + token
        except KeyError as e:
            raise ConfigurationException(str(e) + " from Telegram setup")
        except InvalidSchema as e:
            raise ConfigurationException(str(e) + " from Telegram setup")
        except MissingSchema as e:
            raise ConfigurationException(str(e) + " from Telegram setup")
        except ConnectionError as e:
            raise ConfigurationException(str(e) + " from Telegram setup")

    def send_photo(self, filename="", caption=""):
        method = "/sendPhoto"
        url = self._url + method
        body = {'chat_id': self._channel_id,
                'caption': caption}
        file = {'photo': open(filename, 'rb')}
        r = requests.post(url, data=body, files=file)
        if r.status_code != requests.codes.ok:
            logging.error("Unable to send photo via Telegram using: " + url + " and body: " + str(body) + ", " + r.text)

    def send_text(self, text=""):
        method = "/sendMessage"
        url = self._url + method
        body = {'chat_id': self._channel_id,
                'text': text}
        r = requests.post(url, data=body)
        if r.status_code != requests.codes.ok:
            logging.error("Unable to send text via Telegram using: " + url + " and body: " + str(body) + ", " + r.text)

    def __str__(self):
        return "Telegram"
