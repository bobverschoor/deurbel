import unittest

from deurbel import Deurbel


class DeurbelTest(unittest.TestCase):
    def test_deurbel(self):
        db = Deurbel(config_filename="test-config.toml")



if __name__ == '__main__':
    unittest.main()
