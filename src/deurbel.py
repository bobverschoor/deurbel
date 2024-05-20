import time
import logging
from configuration import Configuration
from device.deurbel_gong import DeurbelGong
from device.deurbel_knop import DeurbelKnop
from device.mqtt_client import MQTT
from gateway.messenger_gateway import MessengerGateway
from gateway.photo_gateway import PhotoGateway
import threading


class Deurbel:
    def __init__(self, timeout=60, config_filename="resources/config.toml"):
        self.timeout = timeout
        self.config_filename = config_filename
        self._gong = None
        self._knop = None
        self._messenger = None
        self._photo_camera = None
        self._home_automation = None

    def setup(self):
        config = Configuration(self.config_filename)
        logging.basicConfig(filename=config.get_log_filename(), encoding='utf-8', level=logging.INFO,
                            format='%(asctime)s %(levelname)s:%(message)s')
        logging.info("======================")
        logging.info("Deurbel setup")
        self._gong = DeurbelGong(config.get_module(config.DEURBEL_GONG))
        self._knop = DeurbelKnop(config.get_module(config.DEURBEL_KNOP), handler=self.deurbel_handler)
        self._photo_camera = PhotoGateway(config.get_module(config.PHOTO_CAMERA))
        self._photo_camera.setup()
        self._messenger = MessengerGateway(config.get_module(config.MESSENGER))
        self._messenger.setup()
        photo_files = self._photo_camera.take()
        if photo_files:
            self._messenger.send(photo_filenames=photo_files, text="Setup")
        else:
            self._messenger.send(photo_filenames=["resources/aanbellen.jpeg"], text="Setup")
        self._home_automation = MQTT(config.get_module(config.HOME_AUTOMATION))
        self._home_automation.setup()
        self._home_automation.trigger()
        logging.info("Deurbel setup finished")

    def deurbel_handler(self, channel):
        if self._knop.pressed(channel):
            gong = threading.Thread(target=self._gong.sound)
            home_automation = threading.Thread(target=self._home_automation.trigger)
            gong.start()
            home_automation.start()
            self._messenger.send(photo_filenames=self._photo_camera.take(), text="Er staat iemand bij de voordeur")
            home_automation.join()
            gong.join()
        else:
            logging.info("Ignoring event from: " + str(channel))

    def main(self):
        self.setup()
        if self._knop.using_mock():
            logging.error("Using DEV version of GPIO. Install GPIO library first!")
            print("Deurbel Stopping due to error: Using DEV version of GPIO")
            raise RuntimeError("Deurbel Stopping due to error: Using DEV version of GPIO")
        logging.info("Entering main loop...")
        while True:
            time.sleep(self.timeout)


if __name__ == '__main__':
    print("Deurbel Starting...")
    deurbel = Deurbel()
    deurbel.main()
