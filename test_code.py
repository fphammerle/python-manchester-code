import pytest

import manchester_code


@pytest.mark.parametrize(
    ("data", "encoded"),
    (
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
    ),
)
def test_encode(data, encoded):
    assert encoded == manchester_code.encode(data)
    assert encoded == manchester_code.encode(bytes(data))
    assert encoded == manchester_code.encode(bytearray(data))
