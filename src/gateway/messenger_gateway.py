import logging
import os

from configuration import Configuration
from device.telegram import Telegram


class MessengerGateway:
    DEVICES = 'devices'
    NAME = 'name'

    def __init__(self, config):
        self._config = config
        self._devices = []
        try:
            self.enabled = config[Configuration.ENABLED]
            if self.DEVICES not in self._config:
                logging.warning("No messenger devices configured, turning messenger off")
                self.enabled = False
            else:
                for device_config in self._config['devices']:
                    if self.NAME not in device_config:
                        logging.warning("Device config has no name, skipping configuring" + str(device_config))
                    else:
                        if device_config[self.NAME] == 'telegram':
                            device = Telegram(device_config)
                            self._devices.append(device)
            if len(self._devices) == 0:
                logging.warning("No messenger devices configured, turning messenger off")
                self.enabled = False
        except KeyError:
            self.enabled = False
            logging.info("Messenger not enabled, configuration missing")

    def setup(self):
        if self.enabled:
            for device in self._devices:
                device.setup()
            logging.info("Messenger enabled: " + str(self.enabled))

    def send(self, text="", photo_filename=""):
        if self.enabled:
            for device in self._devices:
                if photo_filename:
                    if os.path.exists(photo_filename):
                        device.send_photo(filename=photo_filename, caption=text)
                        logging.info("Photo send to device: " + str(device))
                    else:
                        logging.warning("Could not locate photofile: " + str(photo_filename))
                        device.send_text(text)
                        logging.info("Text send to device: " + str(device))
                else:
                    device.send_text(text)
                    logging.info("Text send to device: " + str(device))
