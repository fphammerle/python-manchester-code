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
