from device.mqtt_client import MQTT


class MockMQTT(MQTT):
    def __init__(self):
        self._actions = []
        super().__init__({'enabled': True})

    def trigger(self):
        self._actions.append({'trigger': True})
