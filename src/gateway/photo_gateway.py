import logging

from configuration import Configuration
from device.esp32cam import Esp32Cam


class PhotoGateway:
    DEVICES = 'devices'
    NAME = 'name'

    def __init__(self, config):
        self._config = config
        try:
            self.enabled = config[Configuration.ENABLED]
        except KeyError:
            self.enabled = False
        self._devices = []

    def setup(self):
        if self.enabled:
            if self.DEVICES not in self._config:
                logging.warning("No photo devices configured, turning cameras off")
                self.enabled = False
            else:
                for device_config in self._config['devices']:
                    if self.NAME not in device_config:
                        logging.warning("Device config has no name, skipping configuring" + str(device_config))
                    else:
                        if device_config[self.NAME] == 'esp32cam':
                            device = Esp32Cam(device_config)
                            device.setup()
                            self._devices.append(device)
            if len(self._devices) == 0:
                logging.warning("No photo devices configured, turning cameras off")
                self.enabled = False

    def take(self):
        pass
