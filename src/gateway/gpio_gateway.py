import logging

try:
    import RPi.GPIO as GPIO
except ImportError:
    import RPi_tst.GPIO as GPIO


class RaspberryPiException(Exception):
    def __init__(self, message):
        super(RaspberryPiException, self).__init__(message)


class RaspberryPi:
    VALID_CHANNELS = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 35, 36,
                      37, 38, 40]

    def __init__(self):
        self._gpio = GPIO
        self._gpio.setmode(GPIO.BOARD)
        self._gpio.setwarnings(False)
        self._output_channel = -1

    def setup_input_handler(self, channel_number, callback, bounce_time=200):
        check_channel_number(channel_number)
        self._gpio.setup(channel_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        logging.info("Setting up input to channel: " + str(channel_number) + " and pull_up_down to: " +
                     str(GPIO.PUD_DOWN))
        self._gpio.add_event_detect(channel_number=channel_number, edge=GPIO.RISING, callback=callback,
                                    bouncetime=bounce_time)
        logging.info("adding event detection to: " + str(channel_number) + " edge: " + str(GPIO.RISING) +
                     " callback: " + str(callback) + " bounce time" + str(bounce_time))

    def setup_output_channel(self, channel_number):
        check_channel_number(channel_number)
        self._gpio.setup(channel_number, GPIO.OUT)
        logging.info("setup output to channel: " + str(channel_number))
        self._output_channel = channel_number

    def set_output_high(self):
        if self._output_channel == -1:
            raise RaspberryPiException("Output channel not setup")
        self._gpio.output(self._output_channel, True)

    def set_output_low(self):
        if self._output_channel == -1:
            raise RaspberryPiException("Output channel not setup")
        self._gpio.output(self._output_channel, False)

    def using_mock(self):
        if self._gpio.VERSION == 'mock':
            return True
        return False


def check_channel_number(channel_number):
    if channel_number not in RaspberryPi.VALID_CHANNELS:
        raise RaspberryPiException("Wrong channel number for input: " + str(channel_number))


