import struct

import payload_state


class LaunchDataPacket:
    launch_name: str
    next_sector: int

    def __init__(self, data: bytearray):
        self.launch_name = ""

        name_idx = 0
        while name_idx < 64 and data[name_idx] != 0x00:
            self.launch_name += chr(data[name_idx])
            name_idx += 1

        self.next_sector, = struct.unpack('>I', data[68:72])

    def update_payload_state(self):
        payload_state.current_launch_data = self
        pass
