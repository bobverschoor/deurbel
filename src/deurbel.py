import time
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
        self._gong = DeurbelGong(config.get_module(config.DEURBEL_GONG))
        self._knop = DeurbelKnop(config.get_module(config.DEURBEL_KNOP), handler=self.deurbel_handler)

    def deurbel_handler(self):
        self._gong.sound()

    def main(self):
        self.setup()
        if self._knop.using_mock():
            print("ERROR: Using DEV version of GPIO. Install GPIO library first!")
            exit(1)
        while True:
            time.sleep(self.timeout)


if __name__ == '__main__':
    deurbel = Deurbel()
    deurbel.main()
