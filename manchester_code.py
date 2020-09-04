import typing


def encode(data: typing.Union[bytes, bytearray, typing.List[int]]) -> bytes:
    """
    G. E. Thomas convention
    """
    manchester_code: typing.List[int] = []
    for byte in data:
        manchester_code.extend((0, 0))
        for bit_index in range(7, -1, -1):
            if byte & (0b1 << bit_index):
                bits = 0b10
            else:
                bits = 0b01
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
    raise ValueError("invalid bit 0b{:02b}".format(manchester_bit))


def decode(manchester_code: typing.Union[bytes, bytearray, typing.List[int]]) -> bytes:
    """
    G. E. Thomas convention
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
