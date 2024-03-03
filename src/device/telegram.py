from configuration import ConfigurationException
from utils.requests_wrapper import RequestWrapper, RequestException


class Telegram:
    CONFIG_TOKEN = 'token'
    CONFIG_CHANNEL_ID = 'channel_id'
    CONFIG_BASE_URL = 'base_url'

    def __init__(self, config):
        self._config = config
        self._url = ""
        self._channel_id = ""
        self._request = RequestWrapper(timeout=5, origin=str(self))

    def setup(self):
        try:
            token = self._config[self.CONFIG_TOKEN]
            if not token.startswith('bot'):
                token = "bot" + token
            self._channel_id = self._config[self.CONFIG_CHANNEL_ID]
            base_url = self._config[self.CONFIG_BASE_URL]
            if not base_url.endswith("/"):
                base_url = base_url + "/"
            self._url = base_url + token
            self._request.http_get_text(base_url)
        except KeyError as e:
            raise ConfigurationException(str(e) + " from Telegram setup")
        except RequestException as e:
            raise ConfigurationException(str(e) + " from Telegram setup")

    def send_photo(self, filename="", caption=""):
        method = "/sendPhoto"
        url = self._url + method
        body = {'chat_id': self._channel_id,
                'caption': caption}
        with open(filename, 'rb') as fh:
            file = {'photo': fh}
            try:
                self._request.http_post(url, data=body, files=file)
            except RequestException:
                pass

    def send_text(self, text=""):
        method = "/sendMessage"
        url = self._url + method
        body = {'chat_id': self._channel_id,
                'text': text}
        try:
            self._request.http_post(url, data=body)
        except RequestException:
            pass

    def __str__(self):
        return "Telegram"
