# manchester-code - Python library to encode & decode data as Manchester code
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Encode & decode data as Manchester code <https://en.wikipedia.org/wiki/Manchester_code>
"""

import collections.abc


def encode(data: bytes | bytearray | list[int]) -> bytes:
    """
    G. E. Thomas convention

    >>> manchester_code = encode([0b00001111, 0b01101001])
    >>> ''.join(f'{m:08b}' for m in manchester_code)
    '01010101101010100110100110010110'

    >>> manchester_code = encode(b'msg')
    >>> manchester_code
    b'i\xa6jZij'
    >>> ''.join(f'{m:08b}' for m in manchester_code)
    '011010011010011001101010010110100110100101101010'
    """
    manchester_code: list[int] = []
    for byte in data:
        manchester_code.extend((0, 0))
        for bit_index in range(7, -1, -1):
            bits = 0b10 if (byte & (0b1 << bit_index)) else 0b01
            if bit_index >= 4:
                manchester_code[-2] |= bits << (bit_index * 2 - 8)
            else:
                manchester_code[-1] |= bits << (bit_index * 2)
    return bytes(manchester_code)


def _decode_manchester_bit(manchester_bit: int) -> int:
    if manchester_bit == 0b10:
        return 1
    if manchester_bit == 0b01:
        return 0
    raise ValueError(f"invalid manchester bit 0b{manchester_bit:02b}")


def decode(manchester_code: bytes | bytearray | list[int]) -> bytes:
    """
    G. E. Thomas convention

    >>> data = decode([0b01010101, 0b10101010, 0b01101001, 0b10010110])
    >>> ''.join(f'{m:08b}' for m in data)
    '0000111101101001'

    >>> decode(b'ieiVjeiV')
    b'data'
    """
    data = bytearray()
    for manchester_byte in zip(manchester_code[0::2], manchester_code[1::2]):
        byte = 0
        for bit_index in range(4):
            byte |= (
                _decode_manchester_bit((manchester_byte[1] >> (bit_index * 2)) & 0b11)
                << bit_index
            )
            byte |= (
                _decode_manchester_bit((manchester_byte[0] >> (bit_index * 2)) & 0b11)
                << 4
            ) << bit_index
        data.append(byte)
    return bytes(data)


def _bit_to_int(bit: int | bool) -> int:
    bit = int(bit)
    if bit not in [0, 1]:
        raise ValueError(f"invalid bit {bit!r}, expected 0, False, 1, or True")
    return bit


def decode_bits(
    manchester_code: collections.abc.Iterable[int | bool],
) -> collections.abc.Iterator[bool]:
    """
    G. E. Thomas convention

    >>> list(decode_bits([False, True, True, False, True, False]))
    [False, True, True]
    >>> list(decode_bits([1, 0, 1, 0, 0, 1, 1, 0]))
    [True, True, False, True]
    """
    manchester_code_int = map(_bit_to_int, manchester_code)
    return (
        bool(_decode_manchester_bit((prior << 1) | later))
        for prior, later in zip(iter(manchester_code_int), iter(manchester_code_int))
    )
