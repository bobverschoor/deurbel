import json
import unittest

from configuration import Configuration
from device.mqtt_client import MQTT


class MockMQTTPublish:
    def __init__(self):
        self._actions = []

    def single(self, topic, payload="", hostname="", port=0, auth=None, client_id=""):
        self._actions.append({"single": {"topic": topic, "payload": payload, "hostname": hostname, "port": port,
                                         "auth": auth, "client_id": client_id}})


class TestMQTTClient(unittest.TestCase):
    def test_setup(self):
        mqtt = MQTT({})
        mqtt.setup()
        self.assertFalse(mqtt.enabled)
        mqtt = MQTT({Configuration.ENABLED: True})
        mqtt.setup()
        self.assertFalse(mqtt.enabled)
        mqtt = MQTT({Configuration.ENABLED: True, mqtt.CONFIG_ACTION_TOPIC: "action"})
        mqtt.setup()
        self.assertFalse(mqtt.enabled)
        mqtt = MQTT({Configuration.ENABLED: True, mqtt.CONFIG_CLIENT_ID: 'deurbel', mqtt.CONFIG_PASSWORD: 'secret',
                     mqtt.CONFIG_USERNAME: 'test', mqtt.CONFIG_PORT: 8543, mqtt.CONFIG_HOST: 'localhost',
                     mqtt.CONFIG_ACTION_TOPIC: 'action', mqtt.CONFIG_DISCOVERY_TOPIC: 'discovery'})
        mqtt._mqtt = MockMQTTPublish()
        mqtt.setup()
        self.assertTrue(mqtt.enabled)
        mqtt.trigger()
        disc_payload = {"automation_type": "trigger", "type": "action", "subtype": "button_click",
                        "payload": "button_click", "topic": "action", "device": {"identifiers": ["deurbel"],
                                                                                 "name": "deurbel"}}
        self.assertEqual([{"single": {"topic": "discovery", "payload": json.dumps(disc_payload),
                                      "hostname": "localhost", "port": 8543,
                                      "auth": {"username": "test", "password": "secret"},
                                      "client_id": "deurbel"}},
                          {"single": {"topic": "action", "payload": mqtt.ACTION_PAYLOAD,
                                      "hostname": "localhost", "port": 8543,
                                      "auth": {"username": "test", "password": "secret"},
                                      "client_id": "deurbel"}}
                          ], mqtt._mqtt._actions)
