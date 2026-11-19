"""Python 3 port of original/encryptme.py, used only for testing the decoder.

The original is Python 2 (string.maketrans, xrange, print statement).
This port keeps the same three steps and the same make_secret() logic.
"""
import base64
import codecs
import random
import string


def step1(s):
    return codecs.encode(s, 'rot13')


def step2(s):
    return base64.b64encode(s.encode()).decode()


def step3(s, shift=4):
    lower = string.ascii_lowercase
    return s.translate(str.maketrans(lower, lower[shift:] + lower[:shift]))


STEPS = [step1, step2, step3]


def make_secret(plain, count, rng=random):
    a = '2' + step2(plain)
    for _ in range(count):
        i = rng.randrange(3)
        a = str(i + 1) + STEPS[i](a)
    return a
