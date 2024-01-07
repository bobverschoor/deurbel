import time

import gpio_gateway


class DeurbelGong:
    CONFIG_DURATION = "gong_duration_ms"
    CONFIG_CHANNEL_NUMBER = "gpio_channel"

    def __init__(self, configuration):
        self._duration = configuration[DeurbelGong.CONFIG_DURATION]
        self._pi = gpio_gateway.RaspberryPi()
        self._pi.setup_output_channel(configuration[DeurbelGong.CONFIG_CHANNEL_NUMBER])

    def sound(self):
        try:
            self._pi.set_output_high()
            time.sleep(self._duration)
        finally:
            self.silence()

    def silence(self):
        self._pi.set_output_low()
