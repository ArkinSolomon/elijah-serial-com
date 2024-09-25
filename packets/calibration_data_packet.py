from calibration_data import CalibrationData
import payload_state


class CalibrationDataPacket:
    calibration_data = CalibrationData()

    # noinspection PyPep8Naming
    def __init__(self, data: bytearray):
        signs = data[0]

        is_AC1_negative = signs & 0x80 > 0
        is_AC2_negative = signs & 0x40 > 0
        is_AC3_negative = signs & 0x20 > 0
        is_B1_negative = signs & 0x10 > 0
        is_B2_negative = signs & 0x08 > 0
        is_MB_negative = signs & 0x04 > 0
        is_MC_negative = signs & 0x02 > 0
        is_MD_negative = signs & 0x01 > 0

        self.calibration_data.AC1 = (data[1] << 8 | data[2]) * (1 if is_AC1_negative else -1)
        self.calibration_data.AC2 = (data[3] << 8 | data[4]) * (1 if is_AC2_negative else -1)
        self.calibration_data.AC3 = (data[5] << 8 | data[6]) * (1 if is_AC3_negative else -1)
        self.calibration_data.AC4 = (data[7] << 8 | data[8])
        self.calibration_data.AC5 = (data[9] << 8 | data[10])
        self.calibration_data.AC6 = (data[11] << 8 | data[12])
        self.calibration_data.B1 = (data[13] << 8 | data[14]) * (1 if is_B1_negative else -1)
        self.calibration_data.B2 = (data[15] << 8 | data[16]) * (1 if is_B2_negative else -1)
        self.calibration_data.MB = (data[17] << 8 | data[18]) * (1 if is_MB_negative else -1)
        self.calibration_data.MC = (data[19] << 8 | data[20]) * (1 if is_MC_negative else -1)
        self.calibration_data.MD = (data[21] << 8 | data[22]) * (1 if is_MD_negative else -1)

    def update_payload_state(self):
        payload_state.calibration_data = self.calibration_data
