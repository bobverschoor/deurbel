import logging
import time
from datetime import datetime

from gateway import gpio_gateway
from configuration import ConfigurationException, Configuration


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
        self._pi = gpio_gateway.RaspberryPi()
        self._pi.setup_output_channel(configuration[DeurbelGong.CONFIG_CHANNEL_NUMBER])
        if DeurbelGong.CONFIG_SILENCE_WINDOW in configuration:
            self._silence_window_start, self._silence_window_end = configuration[DeurbelGong.CONFIG_SILENCE_WINDOW]
            if not (is_valid_hour(self._silence_window_start) and is_valid_hour(self._silence_window_end)):
                raise ConfigurationException("Invalid start or end silence window, should be between 0-23, " +
                                             str(self._silence_window_start) + " : " + str(self._silence_window_end))

    def sound(self):
        if self.enabled:
            logging.info("Bel gaat")
            try:
                self._pi.set_output_high()
                time.sleep(self._duration_ms / 1000)
            finally:
                self.silence()

    def silence(self):
        if self.enabled:
            self._pi.set_output_low()

    def silence_window(self):
        now = datetime.now()
        if self._silence_window_start == 0 and self._silence_window_end == 0:
            return False
        return True


def is_valid_hour(hour):
    try:
        if 0 <= hour <= 23:
            return True
        else:
            return False
    except TypeError:
        return False
