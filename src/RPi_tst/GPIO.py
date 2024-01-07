# Puur voor ontwikkelingsdoeleinden. Deze wordt conditional imported

PUD_DOWN = 1
BOARD = 1
IN = 1
OUT = 2
HIGH = 1
LOW = 0

VERSION = 'mock'

actions = []


def setwarnings(value):
    print("warnings set to: " + str(value))
    actions.append({'setwarnings': value})


def setmode(value):
    print("mode set to: " + str(value))
    actions.append({'setmode': value})


def setup(pin, io, pull_up_down=PUD_DOWN):
    print("setup set to pin:" + str(pin) + ", io:" + str(io) + ", pull_up_down:" + str(pull_up_down))
    actions.append({'setup': {'pin': pin, 'io': io, 'pull_up_down': pull_up_down}})


def output(pin, value):
    print("set output pin: " + str(pin) + " to " + str(value))
    actions.append({'output': {'pin': pin, 'value': value}})


def add_event_callback(channel_number, callback, bouncetime=0):
    print("add_event_callback on pin: " + str(channel_number) + " to callback: " + str(callback) + " with bouncetime: "
          + str(bouncetime))
    actions.append({'add_event_callback':
                        {"channel_number": channel_number, "callback": callback, "bouncetime": bouncetime}})
