import logging
import time

from gateway import gpio_gateway
from configuration import ConfigurationException, Configuration


class DeurbelGong:
    CONFIG_DURATION = "gong_duration_ms"
    CONFIG_CHANNEL_NUMBER = "gpio_channel"

    def __init__(self, configuration):
        self.enabled = configuration[Configuration.ENABLED]
        self._duration_ms = configuration[DeurbelGong.CONFIG_DURATION]
        if self._duration_ms > 10000 or self._duration_ms < 0:
            raise ConfigurationException("gong duration exceeds limits, should be between 0 - 10 seconds: "
                                         + str(self._duration_ms))
        self._pi = gpio_gateway.RaspberryPi()
        self._pi.setup_output_channel(configuration[DeurbelGong.CONFIG_CHANNEL_NUMBER])

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
