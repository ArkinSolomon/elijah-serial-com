import struct
from datetime import datetime, timedelta
import payload_state

class CollectionDataPacket:
    collection_time: datetime | None
    day_of_week: int

    pressure: int
    temperature: float
    altitude: float
    accel_x: float
    accel_y: float
    accel_z: float
    bat_voltage: float
    bat_percent: float

    def __init__(self, data: bytearray):
        seconds = data[0]
        minutes = data[1]
        hours = data[2]

        self.day_of_week = data[3]

        date = data[4]
        month = data[5]
        year = data[6] << 8 | data[7]

        # noinspection PyBroadException
        try:
            self.collection_time = datetime(year, month, date, hours, minutes, seconds)
        except:
            self.collection_time = None

        self.pressure = int.from_bytes(data[8:12])
        self.temperature, self.altitude, self.accel_x, self.accel_y, self.accel_z, self.bat_voltage, self.bat_percent = struct.unpack("<7d", data[12:])

    def update_payload_state(self):
        payload_state.time = self.collection_time
        payload_state.day_of_week = self.day_of_week
        payload_state.pressure = self.pressure
        payload_state.temperature = self.temperature
        payload_state.altitude = self.altitude
        payload_state.accel_x = self.accel_x
        payload_state.accel_y = self.accel_y
        payload_state.accel_z = self.accel_z
        payload_state.bat_voltage = self.bat_voltage
        payload_state.bat_percent = self.bat_percent