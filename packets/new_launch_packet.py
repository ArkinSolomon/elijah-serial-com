from packets.packet_types import PacketTypes, packet_lens


class NewLaunchPacket:
    launch_name: str

    def __init__(self, launch_name: str):
        self.launch_name = launch_name

    def serialize(self) -> bytearray:
        packet = bytearray()
        packet.extend(map(ord, self.launch_name))
        while len(packet) < packet_lens[PacketTypes.NEW_LAUNCH]:
            packet.append(0x00)

        packet.insert(0, PacketTypes.NEW_LAUNCH)
        return packet