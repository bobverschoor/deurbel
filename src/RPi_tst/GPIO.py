# Puur voor ontwikkelingsdoeleinden. Deze wordt conditional imported

PUD_DOWN = 21
PUD_UP = 22
PUD_OFF = 20
BOARD = 1
IN = 1
OUT = 2
HIGH = 1
LOW = 0
RISING = 31
FALLING = 32
BOTH = 33

VERSION = 'mock'

actions = []


def setwarnings(value):
    actions.append({'setwarnings': value})


def setmode(value):
    actions.append({'setmode': value})


def setup(pin, io, pull_up_down=""):
    actions.append({'setup': {'pin': pin, 'io': io, 'pull_up_down': pull_up_down}})


def output(pin, value):
    actions.append({'output': {'pin': pin, 'value': value}})


def add_event_detect(channel_number, edge, callback=None, bouncetime=0):
    actions.append({'add_event_detect':
                        {"channel_number": channel_number, "edge": edge, "callback": callback,
                         "bouncetime": bouncetime}})


def input(channel):
    return HIGH