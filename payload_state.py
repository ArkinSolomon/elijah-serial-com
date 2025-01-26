from datetime import datetime

from ack_status import AckStatus
from calibration_data_bmp_280 import CalibrationDataBMP280
from log_buffer import LogBuffer
from packets.calibration_data_mpu_6050_packet import CalibrationDataMPU6050Packet
from packets.fault_data_packet import FaultDataPacket
from packets.launch_data_packet import LaunchDataPacket

time: datetime | None = None
day_of_week: int = 0

pressure: int = -1
temperature: float = -1
altitude: float = -1

accel_x: float = -1
accel_y: float = -1
accel_z: float = -1

gyro_x: float = -1
gyro_y: float = -1
gyro_z: float = -1

bat_voltage: float = -1
bat_percent: float = -1

calibration_data_bmp_280: CalibrationDataBMP280 | None = None
calibration_data_mpu_6050: CalibrationDataMPU6050Packet | None = None

time_set_ack_status = AckStatus.NOT_WAITING
clear_time_set_ack_status_at: datetime | None = None

calibration_data_ack_status = AckStatus.NOT_WAITING
clear_calibration_data_ack_status_at: datetime | None = None

update_baro_press_ack_status = AckStatus.NOT_WAITING
clear_update_baro_press_ack_status_at: datetime | None = None

last_main_loop_time: int = -100
last_core_1_loop_time: int = -100
last_usb_loop_time: int = -100

log_messages = LogBuffer()

last_fault_data: FaultDataPacket | None = None
current_launch_data: LaunchDataPacket | None = None

def clear_messages():
    global log_messages
    log_messages.unfreeze()
    log_messages = LogBuffer()


def reset_state() -> None:
    global time, day_of_week, pressure, temperature, altitude, calibration_data_bmp_280, calibration_data_mpu_6050, last_main_loop_time, accel_x, accel_y, accel_z, current_launch_data
    global time_set_ack_status, clear_time_set_ack_status_at, calibration_data_ack_status, clear_calibration_data_ack_status_at, update_baro_press_ack_status, clear_update_baro_press_ack_status_at
    time = None
    day_of_week = 0
    pressure = -1
    temperature = -1
    altitude = -1
    accel_x = -1
    accel_y = -1
    accel_z = -1
    calibration_data_mpu_6050 = None
    calibration_data_bmp_280 = None

    time_set_ack_status = AckStatus.NOT_WAITING
    clear_time_set_ack_status_at = None

    calibration_data_ack_status = AckStatus.NOT_WAITING
    clear_calibration_data_ack_status_at = None

    update_baro_press_ack_status = AckStatus.NOT_WAITING
    clear_update_baro_press_ack_status_at = None
    current_launch_data = None

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
