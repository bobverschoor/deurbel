import gpio_gateway


class DeurbelKnop:
    CONFIG_CHANNEL_NUMBER = "gpio_channel"
    CONFIG_BOUNCE_TIME = "bounce_time_ms"

    def __init__(self, configuration, handler):
        self._pi = gpio_gateway.RaspberryPi()
        self._pi.setup_input_handler(configuration[DeurbelKnop.CONFIG_CHANNEL_NUMBER], handler,
                                     configuration[DeurbelKnop.CONFIG_BOUNCE_TIME])
