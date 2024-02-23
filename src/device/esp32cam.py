class Esp32Cam:
    def __init__(self, config):
        self._config = config
        self._url = ""
        self._channel_id = ""

    def setup(self):
        pass

    def __str__(self):
        return "Esp32Cam"
