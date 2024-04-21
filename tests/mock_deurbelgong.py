from configuration import Configuration
from device.deurbel_gong import DeurbelGong


class MockDeurbelGong(DeurbelGong):
    def __init__(self):
        self._actions = []
        super().__init__({Configuration.ENABLED: True, DeurbelGong.CONFIG_DURATION: 0,
                          DeurbelGong.CONFIG_CHANNEL_NUMBER: 8})

    def sound(self):
        self._actions.append({'sound': True})
