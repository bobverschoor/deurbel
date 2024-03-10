from utils.requests_wrapper import RequestWrapper, RequestException


class MockRequestWrapper(RequestWrapper):
    def __init__(self):
        super().__init__()
        self._actions = []
        self._get_text_response = ""

    def _post(self, url, data=None, files=None):
        if 'caption' in data and data['caption'] == 'Exception':
            self._actions.append({"raised": "RequestException"})
            raise RequestException("test")
        elif 'text' in data and data['text'] == 'Exception':
            self._actions.append({"raised": "RequestException"})
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

    def http_get_stream(self, url):
        self._actions.append({"action": "http_get_stream", "url": url})
        return bytes()
