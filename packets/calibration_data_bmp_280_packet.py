import struct

import payload_state as payload_state
from calibration_data_bmp_280 import CalibrationDataBMP280


class CalibrationDataBMP280Packet:
    calibration_data = CalibrationDataBMP280()

    # noinspection PyPep8Naming
    def __init__(self, data: bytearray):
        signs = data[0]

        is_T2_negative = signs & 0x80 > 0
        is_T3_negative = signs & 0x40 > 0
        is_P2_negative = signs & 0x20 > 0
        is_P3_negative = signs & 0x10 > 0
        is_P4_negative = signs & 0x08 > 0
        is_P5_negative = signs & 0x04 > 0
        is_P6_negative = signs & 0x02 > 0
        is_P7_negative = signs & 0x01 > 0

        signs = data[1]
        is_P8_negative = signs & 0x02 > 0
        is_P9_negative = signs & 0x01 > 0

        self.calibration_data.dig_T1 = (data[2] << 8 | data[3])
        self.calibration_data.dig_T2 = (data[4] << 8 | data[5]) * (-1 if is_T2_negative else 1)
        self.calibration_data.dig_T3 = (data[6] << 8 | data[7]) * (-1 if is_T3_negative else 1)
        self.calibration_data.dig_P1 = (data[8] << 8 | data[9])
        self.calibration_data.dig_P2 = (data[10] << 8 | data[11]) * (-1 if is_P2_negative else 1)
        self.calibration_data.dig_P3 = (data[12] << 8 | data[13]) * (-1 if is_P3_negative else 1)
        self.calibration_data.dig_P4 = (data[14] << 8 | data[15]) * (-1 if is_P4_negative else 1)
        self.calibration_data.dig_P5 = (data[16] << 8 | data[17]) * (-1 if is_P5_negative else 1)
        self.calibration_data.dig_P6 = (data[18] << 8 | data[19]) * (-1 if is_P6_negative else 1)
        self.calibration_data.dig_P7 = (data[20] << 8 | data[21]) * (-1 if is_P7_negative else 1)
        self.calibration_data.dig_P8 = (data[22] << 8 | data[23]) * (-1 if is_P8_negative else 1)
        self.calibration_data.dig_P9 = (data[24] << 8 | data[25]) * (-1 if is_P9_negative else 1)

        self.calibration_data.baro_pressure = struct.unpack("d", data[26:])[0]

    def update_payload_state(self):
        payload_state.calibration_data_bmp_280 = self.calibration_data
