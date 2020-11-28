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

# pylint: disable=missing-docstring

import pytest

import manchester_code

_DATA_MANCHESTER_CODE_MAPPING = (
    ([0b00000000], [0b01010101, 0b01010101]),
    ([0b11111111], [0b10101010, 0b10101010]),
    ([0b01101001], [0b01101001, 0b10010110]),
    ([0b11101000], [0b10101001, 0b10010101]),
    ([0b01011010], [0b01100110, 0b10011001]),
    (
        [0b11111111, 0b00000000, 0b01101001],
        [0b10101010, 0b10101010, 0b01010101, 0b01010101, 0b01101001, 0b10010110],
    ),
    (
        [0b01101001, 0b11111111, 0b00000000],
        [0b01101001, 0b10010110, 0b10101010, 0b10101010, 0b01010101, 0b01010101],
    ),
)


@pytest.mark.parametrize(("data", "code"), _DATA_MANCHESTER_CODE_MAPPING)
def test_encode(data, code):
    assert bytes(code) == manchester_code.encode(data)
    assert bytes(code) == manchester_code.encode(bytes(data))
    assert bytes(code) == manchester_code.encode(bytearray(data))


@pytest.mark.parametrize(("data", "code"), _DATA_MANCHESTER_CODE_MAPPING)
def test_decode(data, code):
    assert bytes(data) == manchester_code.decode(code)
    assert bytes(data) == manchester_code.decode(bytes(code))
    assert bytes(data) == manchester_code.decode(bytearray(code))


def test_decode_invalid():
    with pytest.raises(ValueError):
        manchester_code.decode([0b01010101, 0b01110101])


@pytest.mark.parametrize(
    ("data", "code"),
    [
        ([0], [False, True]),
        ([1], [True, False]),
        ([False], [False, True]),
        ([True], [True, False]),
        ([False, True], [False, True, True, False]),
        ([True, False], [True, False, False, True]),
        ([0, 0, 1, 0], [False, True, False, True, True, False, False, True]),
        ([1, 0, 1, 1], [True, False, False, True, True, False, True, False]),
    ],
)
def test_decode_bits(data, code):
    assert list(manchester_code.decode_bits(code)) == data
    # test support for iterator
    assert list(manchester_code.decode_bits(not b for b in code)) == [
        not b for b in data
    ]


def test_decode_bits_invalid_bit():
    with pytest.raises(ValueError, match=r"^invalid bit 2\b"):
        list(manchester_code.decode_bits([0, 1, 0, 2]))


def test_decode_bits_invalid_manchester_bit():
    with pytest.raises(ValueError, match=r"^invalid manchester bit 0b00$"):
        list(manchester_code.decode_bits([False, True, False, False]))
    with pytest.raises(ValueError, match=r"^invalid manchester bit 0b11$"):
        list(manchester_code.decode_bits([False, True, True, True, False, True]))
