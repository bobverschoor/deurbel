from configuration import Configuration
from device.deurbel_knop import DeurbelKnop


class MockDeurbelKnop(DeurbelKnop):
    def __init__(self):
        self._actions = []
        super().__init__({Configuration.ENABLED: True, DeurbelKnop.CONFIG_BOUNCE_TIME: 500,
                          DeurbelKnop.CONFIG_CHANNEL_NUMBER: 7, DeurbelKnop.CONFIG_EDGE: 'rising',
                          DeurbelKnop.CONFIG_RESISTOR: 'pull_down'}, handler=None)

    def pressed(self, channel):
        self._actions.append({'pressed': channel})
        return True
