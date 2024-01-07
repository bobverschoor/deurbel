import unittest

from deurbel import Deurbel


class DeurbelTest(unittest.TestCase):
    def test_deurbel(self):
        db = Deurbel(config_filename="test-config.toml")
        db.setup()
        self.assertIsNotNone(db._gong)
        self.assertIsNotNone(db._knop)
        db.deurbel_handler()
        self.assertEqual([{"setmode": 1}, {"setwarnings": False},
                          {"setup": {"pin": 7, "io": 2, "pull_up_down": 1}}, {"setmode": 1}, {"setwarnings": False},
                          {'add_event_callback':
                          {'bouncetime': 500, 'callback': db.deurbel_handler, 'channel_number': 8}},
                          {'output': {'pin': 7, 'value': 1}}, {'output': {'pin': 7, 'value': 0}}],
                         db._gong._pi._gpio.actions)

