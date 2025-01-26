import struct

import payload_state


class CalibrationDataMPU6050Packet:
    diff_xa: float
    diff_ya: float
    diff_za: float

    diff_xg: float
    diff_yg: float
    diff_zg: float

    def __init__(self, data: bytearray):
        self.diff_xa, self.diff_ya, self.diff_za, self.diff_xg, self.diff_yg, self.diff_zg = struct.unpack("<6d", data)

    def upload_payload_state(self):
        payload_state.calibration_data_mpu_6050 = self
