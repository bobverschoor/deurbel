
from gateway import gpio_gateway
from configuration import ConfigurationException, Configuration


class DeurbelKnop:
    CONFIG_CHANNEL_NUMBER = "gpio_channel"
    CONFIG_BOUNCE_TIME = "bounce_time_ms"

    def __init__(self, configuration, handler):
        if not configuration[Configuration.ENABLED]:
            raise ConfigurationException("Mandatory module deurbel_knop is not enabled in configuration")
        self._pi = gpio_gateway.RaspberryPi()
        if configuration[DeurbelKnop.CONFIG_BOUNCE_TIME] > 1000 or configuration[DeurbelKnop.CONFIG_BOUNCE_TIME] < 0:
            raise ConfigurationException("Bounce time not within boundaries (0, 1000): " +
                                         str(configuration[DeurbelKnop.CONFIG_BOUNCE_TIME]))
        self._configured_channel = configuration[DeurbelKnop.CONFIG_CHANNEL_NUMBER]
        self._pi.setup_input_handler(configuration[DeurbelKnop.CONFIG_CHANNEL_NUMBER], handler,
                                     configuration[DeurbelKnop.CONFIG_BOUNCE_TIME])

    def pressed(self, channel):
        if channel == self._configured_channel:
            return True
        return False

    def using_mock(self):
        return self._pi.using_mock()
