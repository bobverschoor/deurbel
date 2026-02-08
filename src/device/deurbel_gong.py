import logging
import time
from configuration import ConfigurationException, Configuration
from gpiozero import Buzzer

class DeurbelGong:
    CONFIG_DURATION = "gong_duration_ms"
    CONFIG_CHANNEL_NUMBER = "gpio_channel"
    CONFIG_SILENCE_WINDOW = "silence_window"

    def __init__(self, configuration):
        self.enabled = configuration[Configuration.ENABLED]
        self._duration_ms = configuration[DeurbelGong.CONFIG_DURATION]
        self._silence_window_start = self._silence_window_end = 0
        if self._duration_ms > 10000 or self._duration_ms < 0:
            raise ConfigurationException("gong duration exceeds limits, should be between 0 - 10 seconds: "
                                         + str(self._duration_ms))
        bcm_nr = "BOARD" + str(configuration[DeurbelGong.CONFIG_CHANNEL_NUMBER])
        self._gong = Buzzer(bcm_nr)

    def sound(self):
        if self.enabled:
            logging.info("Bel gaat")
            try:
                self._gong.on()
                time.sleep(self._duration_ms / 1000)
            finally:
                self.silence()

    def silence(self):
        if self.enabled:
            self._gong.off()
