import struct
from datetime import datetime, timedelta
import payload_state

class CollectionDataPacket:
    collection_time: datetime | None
    day_of_week: int

    pressure: int
    temperature: float
    altitude: float

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
        self.temperature = struct.unpack("d", data[12:20])[0]
        self.altitude = struct.unpack("d", data[20:28])[0]

    def update_payload_state(self):
        payload_state.time = self.collection_time
        payload_state.day_of_week = self.day_of_week
        payload_state.pressure = self.pressure
        payload_state.temperature = self.temperature
        payload_state.altitude = self.altitude