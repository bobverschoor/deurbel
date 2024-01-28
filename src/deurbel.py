import time
import logging
from configuration import Configuration
from deurbel_gong import DeurbelGong
from deurbel_knop import DeurbelKnop


class Deurbel:
    def __init__(self, timeout=60, config_filename="resources/config.toml"):
        self.timeout = timeout
        self.config_filename = config_filename
        self._gong = None
        self._knop = None

    def setup(self):
        config = Configuration(self.config_filename)
        logging.basicConfig(filename=config.get_log_filename(), encoding='utf-8', level=logging.INFO,
                            format='%(asctime)s %(levelname)s:%(message)s')
        logging.info("======================")
        logging.info("Deurbel starting")
        self._gong = DeurbelGong(config.get_module(config.DEURBEL_GONG))
        self._knop = DeurbelKnop(config.get_module(config.DEURBEL_KNOP), handler=self.deurbel_handler)
        logging.info("Deurbel setup finished")

    def deurbel_handler(self):
        self._gong.sound()

    def main(self):
        self.setup()
        if self._knop.using_mock():
            logging.error("Using DEV version of GPIO. Install GPIO library first!")
            print("Deurbel Stopping due to error: Using DEV version of GPIO")
            exit(1)
        while True:
            time.sleep(self.timeout)


if __name__ == '__main__':
    print("Deurbel Starting...")
    deurbel = Deurbel()
    deurbel.main()
