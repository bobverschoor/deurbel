from device.telegram import Telegram


class MockTelegram(Telegram):
    def __init__(self, config=None):
        super().__init__(config)
        self._action = []

    def send_photo(self, filename="", caption=""):
        self._action.append({"method": "send_photo", "filename": filename, "caption": caption})

    def send_text(self, text=""):
        self._action.append({"method": "send_text", "text": text})
