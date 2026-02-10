import logging

from gpiozero import Button
from configuration import ConfigurationException, Configuration


class DeurbelKnop:
    CONFIG_CHANNEL_NUMBER = "gpio_channel"
    CONFIG_BCM_PIN_NR = "bcm_pin_nr"
    CONFIG_BOUNCE_TIME = "bounce_time_ms"
    CONFIG_EDGE = "edge_detection"
    CONFIG_RESISTOR = "resistor"
    CONFIG_PULL_UP = "pull_up"

    def __init__(self, configuration, handler):
        if not configuration[Configuration.ENABLED]:
            raise ConfigurationException("Mandatory module deurbel_knop is not enabled in configuration")

        if configuration[DeurbelKnop.CONFIG_BOUNCE_TIME] > 1000 or configuration[DeurbelKnop.CONFIG_BOUNCE_TIME] < 0:
            raise ConfigurationException("Bounce time not within boundaries (0, 1000): " +
                                         str(configuration[DeurbelKnop.CONFIG_BOUNCE_TIME]))
        self._button = Button(pin=configuration[DeurbelKnop.CONFIG_BCM_PIN_NR],
                              bounce_time=configuration[DeurbelKnop.CONFIG_BOUNCE_TIME],
                              pull_up = configuration[DeurbelKnop.CONFIG_PULL_UP] )
        self._button.when_pressed = handler
        print(self._button)


    def pressed(self, channel):
        logging.info("Input: " + str(self._button.value))
        return self._button.is_pressed

