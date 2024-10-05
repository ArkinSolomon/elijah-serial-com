from datetime import datetime, timedelta

from packets.packet_types import PacketTypes


class SetTimePacket:
    def __init__(self):
        self.now = datetime.now(tz=None) + timedelta(milliseconds=200)

    def serialize(self) -> bytearray:
        packet = bytearray()
        packet.append(PacketTypes.TIME_SET.to_bytes(byteorder='little')[0])
        packet.append(self.now.second.to_bytes(1)[0])
        packet.append(self.now.minute.to_bytes(1)[0])
        packet.append(self.now.hour.to_bytes(1)[0])
        packet.append((7 if self.now.weekday() == 5 else ((self.now.weekday() + 2) % 7)).to_bytes(1)[0])
        packet.append(self.now.day.to_bytes(1)[0])
        packet.append(self.now.month.to_bytes(1)[0])

        year = self.now.year.to_bytes(2, byteorder='little')
        packet.append(year[1])
        packet.append(year[0])
        return packet
