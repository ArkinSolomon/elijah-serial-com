class StringPacket:

    bytes: bytes
    string_value: str

    def __init__(self, data: bytearray):
        self.bytes = data
        self.string_value = data.decode("utf-8", errors='replace')

    def __str__(self):
        return self.string_value
