import unittest
from awm.setting import key_to_keycodes


class TestKeycode(unittest.TestCase):

    def test_isupper(self):
        self.assertEqual(key_to_keycodes('q'), 24)
        self.assertEqual(key_to_keycodes('w'), 25)
        self.assertEqual(key_to_keycodes('e'), 26)
        self.assertEqual(key_to_keycodes('r'), 27)
        self.assertEqual(key_to_keycodes('t'), 28)
        self.assertEqual(key_to_keycodes('y'), 29)
        self.assertEqual(key_to_keycodes('u'), 30)
        self.assertEqual(key_to_keycodes('i'), 31)
        self.assertEqual(key_to_keycodes('o'), 32)
        self.assertEqual(key_to_keycodes('p'), 33)
        self.assertEqual(key_to_keycodes('a'), 38)
        self.assertEqual(key_to_keycodes('z'), 52)

if __name__ == '__main__':
    unittest.main()

