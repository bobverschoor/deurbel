# Puur voor ontwikkel doeleinden. Deze wordt conditional imported

PUD_DOWN = 1
BOARD = 1
IN = 1
OUT = 2
HIGH = 1
LOW = 0

print("WARN: Using DEV version of GPIO. If unintential, install GPIO library first!")


def setwarnings(value):
    print("warnings set to: " + str(value))


def setmode(value):
    print("mode set to: " + str(value))


def setup(pin, io, pull_up_down=PUD_DOWN):
    print("setup set to pin:" + str(pin) + ", io:" + str(io) + ", pull_up_down:" + str(pull_up_down))


def input(pin):
    print("return input pin: " + str(pin))
    return pin


def output(pin, waarde):
    print("set output pin: " + str(pin) + " to " + str(waarde))


def add_event_callback(channel_number, callback, bouncetime=0):
    print("add_event_callback on pin: " + str(channel_number) + " to callback: " + str(callback) + " with bouncetime: "
          + str(bouncetime))

