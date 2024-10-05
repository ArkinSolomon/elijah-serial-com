import struct

from packets.packet_types import PacketTypes


class SetSeaLevelPressPacket:
    pressure: float

    def __init__(self, pressure: float):
        self.pressure = pressure

    def serialize(self) -> bytearray:
        packet =  bytearray(struct.pack("<d", self.pressure))
        packet.insert(0, PacketTypes.SET_SEA_LEVEL_PRESS)
        return packet