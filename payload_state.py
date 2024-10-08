from datetime import datetime

from ack_status import AckStatus
from calibration_data_bmp_180 import CalibrationDataBMP180
from calibration_data_bmp_280 import CalibrationDataBMP280
from log_buffer import LogBuffer

time: datetime | None = None
day_of_week: int = 0

pressure: int = -1
temperature: float = -1
altitude: float = -1

calibration_data_bmp_180: CalibrationDataBMP180 | None = None
calibration_data_bmp_280: CalibrationDataBMP280 | None = None

time_set_ack_status = AckStatus.NOT_WAITING
clear_time_set_ack_status_at: datetime | None = None

calibration_data_ack_status = AckStatus.NOT_WAITING
clear_calibration_data_ack_status_at: datetime | None = None

log_messages = LogBuffer()


def clear_messages():
    global log_messages
    log_messages = LogBuffer()


def reset_state() -> None:
    global time, day_of_week, pressure, temperature, altitude, time_set_ack_status, calibration_data_bmp_180, calibration_data_bmp_280, clear_time_set_ack_status_at, calibration_data_ack_status, clear_calibration_data_ack_status_at
    time = None
    day_of_week = 0
    pressure = -1
    temperature = -1
    altitude = -1
    calibration_data_bmp_180 = None
    calibration_data_bmp_280 = None
    time_set_ack_status = AckStatus.NOT_WAITING
    clear_time_set_ack_status_at = None
    calibration_data_ack_status = AckStatus.NOT_WAITING
    clear_calibration_data_ack_status_at = None
    clear_messages()


def sys_day_of_week_str() -> str:
    match day_of_week:
        case 1:
            return "Sunday"
        case 2:
            return "Monday"
        case 3:
            return "Tuesday"
        case 4:
            return "Wednesday"
        case 5:
            return "Thursday"
        case 6:
            return "Friday"
        case 7:
            return "Saturday"
        case _:
            return "Unknown"
