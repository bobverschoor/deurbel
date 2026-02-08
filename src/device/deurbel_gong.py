import logging
import time
from configuration import ConfigurationException, Configuration
from gpiozero import Buzzer

class DeurbelGong:
    CONFIG_DURATION = "gong_duration_ms"
    CONFIG_CHANNEL_NUMBER = "gpio_channel"
    CONFIG_SILENCE_WINDOW = "silence_window"
    CONFIG_BCM_PIN_NR = "bcm_pin_nr"

    def __init__(self, configuration):
        self.enabled = configuration[Configuration.ENABLED]
        self._duration_ms = configuration[DeurbelGong.CONFIG_DURATION]
        self._silence_window_start = self._silence_window_end = 0
        if self._duration_ms > 10000 or self._duration_ms < 0:
            raise ConfigurationException("gong duration exceeds limits, should be between 0 - 10 seconds: "
                                         + str(self._duration_ms))
        self._gong = Buzzer(pin=configuration[DeurbelGong.CONFIG_BCM_PIN_NR])

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
