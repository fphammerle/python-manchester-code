import typing


def encode(data: typing.Union[bytes, bytearray, typing.List[int]]):
    """
    G. E. Thomas
    """
    encoded_data: typing.List[int] = []
    for byte in data:
        encoded_data.extend((0, 0))
        for bit_index in range(7, -1, -1):
            if byte & (0b1 << bit_index):
                bits = 0b10
            else:
                bits = 0b01
            if bit_index >= 4:
                encoded_data[-2] |= bits << (bit_index * 2 - 8)
            else:
                encoded_data[-1] |= bits << (bit_index * 2)
    return encoded_data
