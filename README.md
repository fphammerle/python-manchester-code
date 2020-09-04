# manchester-code

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI Pipeline Status](https://github.com/fphammerle/python-manchester-code/workflows/tests/badge.svg)](https://github.com/fphammerle/python-manchester-code/actions)
[![Last Release](https://img.shields.io/pypi/v/manchester-code.svg)](https://pypi.org/project/manchester-code/#history)
[![Compatible Python Versions](https://img.shields.io/pypi/pyversions/manchester-code.svg)](https://pypi.org/project/manchester-code/)

Python library to encode & decode data as [Manchester code](https://en.wikipedia.org/wiki/Manchester_code)

## Setup

```sh
$ pip3 install --user --upgrade manchester-code
```

## Usage

0-bits translate to low-high, 1-bits to high-low (G. E. Thomas convention).

```python
import manchester-code

manchester_code = encode([0b00001111, 0b01101001])
print(''.join(['{:08b}'.format(m) for m in manchester_code]))
# 01010101101010100110100110010110

encode(b'msg')
# b'i\xa6jZij'

decode([0b01010101, 0b10101010, 0b01101001, 0b10010110])
# 0000111101101001

decode(b'ieiVjeiV')
# b'data'
```
