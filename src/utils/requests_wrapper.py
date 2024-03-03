import logging

import requests
from requests.exceptions import InvalidSchema, MissingSchema, ConnectionError


class RequestException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RequestWrapper:

    def __init__(self, timeout=30, origin=""):
        self._timeout = timeout
        self._origin = origin

    def _get(self, url, parameters=None, stream=False):
        try:
            if parameters:
                r = requests.get(url, params=parameters, timeout=self._timeout, stream=stream)
            elif stream:
                r = requests.get(url, timeout=self._timeout, stream=stream)
            else:
                r = requests.get(url, timeout=self._timeout)
            if r.status_code != requests.codes.ok:
                logging.error("Unable to get data from: " + str(self._origin) + " to: " + url + " with parameters: " +
                              str(parameters) + r.text)
                raise RequestException("Unable to get data from: " + str(self._origin) + " to: " + url +
                                       " with parameters: " + str(parameters) + r.text)
        except InvalidSchema as e:
            raise RequestException(str(e))
        except MissingSchema as e:
            raise RequestException(str(e))
        except ConnectionError as e:
            raise RequestException(str(e))
        return r

    def _post(self, url, data=None, files=None):
        try:
            if data:
                if files:
                    r = requests.post(url, data=data, files=files, timeout=self._timeout)
                else:
                    r = requests.post(url, data=data, timeout=self._timeout)
            else:
                raise RequestException("No files and/or data to post from: " + str(self._origin) + " to: " + url)
            if r.status_code != requests.codes.ok:
                logging.error("Unable to send data from: " + str(self._origin) + " to: " + url + " and body: " +
                              str(data) + ", or files: " + str(files) + r.text)
                raise RequestException("Unable to send data from: " + str(self._origin) + " to: " + url +
                                       " and body: " + str(data) + ", or files: " + str(files) + r.text)
        except InvalidSchema as e:
            raise RequestException(str(e))
        except MissingSchema as e:
            raise RequestException(str(e))
        except ConnectionError as e:
            raise RequestException(str(e))

    def http_get_text(self, url, parameters=None):
        return self._get(url, parameters=parameters).text

    def http_get_json(self, url, parameters=None):
        return self._get(url, parameters=parameters).json()

    def http_get_stream(self, url):
        return self._get(url, stream=True).content

    def http_post(self, url, data=None, files=None):
        return self._post(url, data=data, files=files)
