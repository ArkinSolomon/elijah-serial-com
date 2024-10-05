import payload_state


class LoopTimePacket:
    loop_time: int

    # noinspection PyPep8Naming
    def __init__(self, data: bytearray):
        self.loop_time = data[0] << 0x18 | data[1] << 0x10 | data[2] << 0x08 | data[3]

    def update_payload_state(self):
        payload_state.last_loop_time = self.loop_time
