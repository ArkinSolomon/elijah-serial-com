from datetime import datetime

from ack_status import AckStatus
from calibration_data_bmp_180 import CalibrationDataBMP180
from calibration_data_bmp_280 import CalibrationDataBMP280
from log_buffer import LogBuffer
from packets.fault_data_packet import FaultDataPacket

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

update_sea_level_press_ack_status = AckStatus.NOT_WAITING
clear_update_sea_level_press_ack_status_at: datetime | None = None

last_main_loop_time: int = -100
last_core_1_loop_time: int = -100
last_usb_loop_time: int = -100

log_messages = LogBuffer()

last_fault_data: FaultDataPacket | None = None

def clear_messages():
    global log_messages
    log_messages.unfreeze()
    log_messages = LogBuffer()


def reset_state() -> None:
    global time, day_of_week, pressure, temperature, altitude, calibration_data_bmp_180, calibration_data_bmp_280, last_main_loop_time
    global time_set_ack_status, clear_time_set_ack_status_at, calibration_data_ack_status, clear_calibration_data_ack_status_at, update_sea_level_press_ack_status, clear_update_sea_level_press_ack_status_at
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

    update_sea_level_press_ack_status = AckStatus.NOT_WAITING
    clear_update_sea_level_press_ack_status_at = None

    last_main_loop_time = -100
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
