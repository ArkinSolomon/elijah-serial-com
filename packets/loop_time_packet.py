import struct

import payload_state


class LoopTimePacket:
    main_loop_time: int
    core_1_loop_time: int
    usb_loop_time: int

    def __init__(self, data: bytearray):
        self.main_loop_time, self.core_1_loop_time, self.usb_loop_time = struct.unpack('>QQQ', data)

    def update_payload_state(self):
        payload_state.last_main_loop_time = self.main_loop_time
        payload_state.last_core_1_loop_time = self.core_1_loop_time
        payload_state.last_usb_loop_time = self.usb_loop_time
