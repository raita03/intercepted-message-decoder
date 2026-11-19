"""Decode intercepted.txt by reversing make_secret() from original/encryptme.py.

Usage:
    python3 decrypt.py intercepted.txt
"""
import base64
import codecs
import string
import sys

LOWER = string.ascii_lowercase
UNDO_STEP3 = str.maketrans(LOWER[4:] + LOWER[:4], LOWER)  # shift lowercase back by 4


def undo(digit, s):
    """Reverse one encoding step, picked by the digit that came in front of it."""
    if digit == '1':
        return codecs.decode(s, 'rot13')      # step1 is ROT13, its own inverse
    if digit == '2':
        return base64.b64decode(s).decode()   # step2 is Base64
    if digit == '3':
        return s.translate(UNDO_STEP3)        # step3 shifts lowercase letters by +4
    raise ValueError(f'unexpected step digit: {digit!r}')


def decode(ciphertext):
    """Peel layers until the original '2' + Base64 layer is gone.

    Returns (plaintext, steps), where steps lists the digits in the order
    they were undone (outermost first).
    """
    s = ciphertext.strip()
    steps = []
    while True:
        digit, s = s[0], s[1:]   # the first character says which step was applied last
        s = undo(digit, s)
        steps.append(digit)
        if digit == '2' and s[:1] not in ('1', '2', '3'):
            return s, steps


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python3 decrypt.py <file>')
    with open(sys.argv[1]) as f:
        plaintext, steps = decode(f.read())
    print('Layers peeled:', len(steps), '| count =', len(steps) - 1)
    print('Secret:', plaintext)


if __name__ == '__main__':
    main()
