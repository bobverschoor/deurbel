from utils.requests_wrapper import RequestWrapper, RequestException


class MockRequestWrapper(RequestWrapper):
    def __init__(self):
        super().__init__()
        self._actions = []
        self._get_text_response = ""

    def _get(self, url, parameters=None, stream=False):
        self._actions.append({"action": "_get", "url": url, "parameters": parameters, "stream": stream})
        return self._get_text_response

    def _post(self, url, data=None, files=None):
        if 'caption' in data and data['caption'] == 'Exception':
            raise RequestException("test")
        if files:
            if 'photo' in files:
                filename = files['photo'].name
                files['photo'].close()
                files['photo'] = filename
        self._actions.append({"action": "_post", "url": url, "data": data, "files": files})

    def http_get_json(self, url, parameters=None):
        self._actions.append({"action": "http_get_json", "url": url, "parameters": parameters})
        return {}

    def http_get_text(self, url, parameters=None):
        self._actions.append({"action": "http_get_text", "url": url, "parameters": parameters})
        return self._get_text_response
