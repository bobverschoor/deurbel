import json
import logging

import paho.mqtt.publish as mqtt

from configuration import Configuration, ConfigurationException


class MQTT:
    CONFIG_USERNAME = "username"
    CONFIG_PASSWORD = "password"
    CONFIG_HOST = "host"
    CONFIG_PORT = "port"
    CONFIG_DISCOVERY_TOPIC = "discovery_topic"
    CONFIG_ACTION_TOPIC = "action_topic"
    CONFIG_CLIENT_ID = "client_id"
    ACTION_PAYLOAD = "button_click"

    def __init__(self, config):
        self._config = config
        self._discovery_payload = {}
        if Configuration.ENABLED in config:
            self.enabled = config[Configuration.ENABLED]
        else:
            self.enabled = False
        self._mqtt = mqtt

    def setup(self):
        try:
            if self.enabled:
                discovery_payload = {"automation_type": "trigger",
                                     "type": "action",
                                     "subtype": self.ACTION_PAYLOAD,
                                     "payload": self.ACTION_PAYLOAD,
                                     "topic": self._config[self.CONFIG_ACTION_TOPIC],
                                     "device": {
                                         "identifiers": [
                                             self._config[self.CONFIG_CLIENT_ID]
                                         ],
                                         "name": self._config[self.CONFIG_CLIENT_ID]
                                     }
                                     }
                self._mqtt.single(self._config[self.CONFIG_DISCOVERY_TOPIC], payload=json.dumps(discovery_payload),
                                  hostname=self._config[self.CONFIG_HOST], port=self._config[self.CONFIG_PORT],
                                  auth={'username': self._config[self.CONFIG_USERNAME],
                                        'password': self._config[self.CONFIG_PASSWORD]},
                                  client_id=self._config[self.CONFIG_CLIENT_ID])
        except KeyError as e:
            logging.error(e)
            self.enabled = False

    def trigger(self):
        if self.enabled:
            self._mqtt.single(self._config[self.CONFIG_ACTION_TOPIC], payload=self.ACTION_PAYLOAD,
                              hostname=self._config[self.CONFIG_HOST], port=self._config[self.CONFIG_PORT],
                              auth={'username': self._config[self.CONFIG_USERNAME],
                                    'password': self._config[self.CONFIG_PASSWORD]},
                              client_id=self._config[self.CONFIG_CLIENT_ID])
