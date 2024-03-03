import logging
import os
from datetime import datetime

from configuration import Configuration
from device.esp32cam import Esp32Cam


class PhotoGateway:
    DEVICES = 'devices'
    NAME = 'name'

    def __init__(self, config):
        self._config = config
        try:
            self.enabled = config[Configuration.ENABLED]
            self._temp_dir = config[Configuration.TEMP_DIR]
        except KeyError:
            self.enabled = False
        self._devices = []
        if PhotoGateway.DEVICES in self._config:
            for device_config in self._config[PhotoGateway.DEVICES]:
                if self.NAME not in device_config:
                    logging.warning("Device config has no name, skipping configuring" + str(device_config))
                else:
                    if device_config[self.NAME] == 'esp32cam':
                        device = Esp32Cam(device_config)
                        self._devices.append(device)
        if len(self._devices) == 0:
            logging.warning("No photo devices configured, turning cameras off")
            self.enabled = False

    def setup(self):
        if self.enabled:
            if self.DEVICES not in self._config:
                logging.warning("No photo devices configured, disabling cameras")
                self.enabled = False
            else:
                if not os.path.exists(self._temp_dir):
                    os.mkdir(self._temp_dir)
                for device in self._devices:
                    device.setup()

    def take(self):
        photo_files = []
        if self.enabled:
            now = datetime.now()
            for device in self._devices:
                file_path = os.path.join(self._temp_dir, str(device) +
                                         datetime.strftime(now, '%Y-%m-%dT%H-%M-%S-%s'))
                photo_files.append(device.capture(file_path))
        return photo_files
