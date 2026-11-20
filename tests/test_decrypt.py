"""Run from the repo root with:  python3 -m unittest discover tests"""
import os
import random
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from decrypt import decode          # noqa: E402
from encrypt_py3 import make_secret, STEPS  # noqa: E402


class TestDecrypt(unittest.TestCase):

    def test_intercepted_message(self):
        with open(os.path.join(ROOT, 'intercepted.txt')) as f:
            plaintext, steps = decode(f.read())
        self.assertEqual(plaintext, 'Why do elephants have big ears?')
        self.assertEqual(len(steps) - 1, 67)

    def test_reencode_matches_intercepted(self):
        # Re-apply the recovered steps to the recovered secret.
        # If we rebuild the intercepted file exactly, the decode is proven.
        with open(os.path.join(ROOT, 'intercepted.txt')) as f:
            original = f.read().strip()
        plaintext, steps = decode(original)
        a = '2' + STEPS[1](plaintext)
        for digit in reversed(steps[:-1]):
            a = digit + STEPS[int(digit) - 1](a)
        self.assertEqual(a, original)

    def test_round_trip(self):
        rng = random.Random(42)
        for count in (0, 1, 5, 30, 67):
            msg = 'Testing message number %d' % count
            plaintext, steps = decode(make_secret(msg, count, rng))
            self.assertEqual(plaintext, msg)
            self.assertEqual(len(steps) - 1, count)


if __name__ == '__main__':
    unittest.main()
