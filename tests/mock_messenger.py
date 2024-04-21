from gateway.messenger_gateway import MessengerGateway


class MockMessenger(MessengerGateway):
    def __init__(self):
        self._actions = []
        super().__init__({})

    def send(self, photo_filenames="", text=""):
        self._actions.append({'send': "photo_filenames=" + photo_filenames + ", text=" + text})
