import struct

from packets.packet_types import PacketTypes


class SetBaroPressPacket:
    pressure: float

    def __init__(self, pressure: float):
        self.pressure = pressure

    def serialize(self) -> bytearray:
        packet =  bytearray(struct.pack("<d", self.pressure))
        packet.insert(0, PacketTypes.SET_BARO_PRESS)
        return packet