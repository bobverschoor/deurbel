from gateway.photo_gateway import PhotoGateway


class MockPhotoCamera(PhotoGateway):
    def __init__(self):
        self._actions = []
        super().__init__({})

    def take(self):
        self._actions.append({'take': True})
        return "photo.jpg"
