# Intercepted message decoder

Group lab, MSc in Computing (Applied Cybersecurity), TU Dublin.

We were given `encryptme.py`, the program believed to have encoded an intercepted message, and the encoded output in `intercepted.txt`. Parts of the program were damaged. This repo holds our decoder.

**Result:** the message is `Why do elephants have big ears?`. The damaged `count` value was 67.

## Files

| File | What it is |
| --- | --- |
| `original/encryptme.py` | The damaged encoder, as given (Python 2) |
| `intercepted.txt` | The intercepted message, 35,138 characters |
| `decrypt.py` | Our decoder (Python 3) |
| `encrypt_py3.py` | A Python 3 port of the encoder, used only by the tests |
| `tests/test_decrypt.py` | Checks the decoded message and runs encode/decode round trips |

## How to run

Needs Python 3.6 or later. No extra packages.

```
python3 decrypt.py intercepted.txt
```

Output:

```
Layers peeled: 68 | count = 67
Secret: Why do elephants have big ears?
```

Run the tests:

```
python3 -m unittest discover tests
```

## How it works

The encoder Base64-encodes the secret and puts `2` in front. Then it loops `count` times. Each time it picks step 1, 2 or 3 at random, applies it to the whole string and puts the step number in front.

| Digit | Encoding step | How we undo it |
| --- | --- | --- |
| 1 | ROT13 | ROT13 again |
| 2 | Base64 encode | Base64 decode |
| 3 | Lowercase letters shifted forward by 4 | Shift them back by 4 |

So the first character of the output always names the last step used. Our decoder reads that digit, strips it, undoes the step and repeats. It stops after a Base64 decode that leaves no 1, 2 or 3 at the front, because that layer is the original `2` + Base64.

One limit: if a secret itself started with 1, 2 or 3, this stop rule would end too late. It doesn't affect this message.

## Why the scheme is weak

There is no key. All three steps are public transforms, and the encoder writes the order of the steps into the output, so anyone with the source can reverse it. Running 67 rounds only made the message about 1,100 times longer.
