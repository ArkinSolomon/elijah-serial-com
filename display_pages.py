import payload_state
from packets.fault_data_packet import FaultDataPacket


def get_display_str(last_fault_data: FaultDataPacket | None, did_fault: bool) -> str:
    if last_fault_data is None:
        return 'Unknown'
    else:
        return 'Fault' if did_fault else 'OK'


class DisplayPageInformation:
    selected_page = 0
    pages: [[(str, str, str)]]

    def __init__(self):
        self.update_pages()

    def update_pages(self):
        self.pages = self.__get_data_pages() + self.__get_calibration_pages() + self.__get_fault_pages()

    def __get_data_pages(self) -> [[(str, str, str)]]:
        return [
            [
                ('Pressure', payload_state.pressure, 'Pa'),
                ('Temperature', payload_state.temperature, '°C'),
                ('Altitude', payload_state.altitude, 'm'),
                ('Acceleration X', payload_state.accel_x, 'm/s^2'),
                ('Acceleration Y', payload_state.accel_y, 'm/s^2'),
                ('Acceleration Z', payload_state.accel_z, 'm/s^2'),
            ]
        ]

    def __get_calibration_pages(self) -> [[(str, str, str)]]:
        return [
            [
                ('T1',
                 payload_state.calibration_data_bmp_280.dig_T1 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('T2',
                 payload_state.calibration_data_bmp_280.dig_T2 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('T3',
                 payload_state.calibration_data_bmp_280.dig_T3 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P1',
                 payload_state.calibration_data_bmp_280.dig_P1 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P2',
                 payload_state.calibration_data_bmp_280.dig_P2 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P3',
                 payload_state.calibration_data_bmp_280.dig_P3 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P4',
                 payload_state.calibration_data_bmp_280.dig_P4 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P5',
                 payload_state.calibration_data_bmp_280.dig_P5 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P6',
                 payload_state.calibration_data_bmp_280.dig_P6 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P7',
                 payload_state.calibration_data_bmp_280.dig_P7 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P8',
                 payload_state.calibration_data_bmp_280.dig_P8 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('P9',
                 payload_state.calibration_data_bmp_280.dig_P9 if payload_state.calibration_data_bmp_280 is not None else -1,
                 ''),
                ('Sea Level Pressure',
                 payload_state.calibration_data_bmp_280.sea_level_pressure if payload_state.calibration_data_bmp_280 is not None else -1,
                 'Pa'),
            ]
        ]

    def __get_fault_pages(self) -> [[(str, str, str)]]:
        return [
            [
                ('Status',
                 f'0x{payload_state.last_fault_data.device_status.to_bytes(length=4, byteorder='big').hex().upper()}' if payload_state.last_fault_data is not None else 'Unknown',
                 '' if payload_state.last_fault_data is not None else 'FAULT_UNIT'),
                ('BMP 280', get_display_str(payload_state.last_fault_data,
                                            payload_state.last_fault_data.fault_bmp_280 if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
                ('DS 1307', get_display_str(payload_state.last_fault_data,
                                            payload_state.last_fault_data.fault_ds_1307 if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
                ('MPU 6050', get_display_str(payload_state.last_fault_data,
                                             payload_state.last_fault_data.fault_mpu_6050 if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
                ('W25Q64FV', get_display_str(payload_state.last_fault_data,
                                             payload_state.last_fault_data.fault_w25q64fv if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
                ('I2C0', get_display_str(payload_state.last_fault_data,
                                         payload_state.last_fault_data.fault_i2c_bus0 if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
                ('I2C1', get_display_str(payload_state.last_fault_data,
                                         payload_state.last_fault_data.fault_i2c_bus1 if payload_state.last_fault_data is not None else False),
                 'FAULT_UNIT'),
            ]
        ]
