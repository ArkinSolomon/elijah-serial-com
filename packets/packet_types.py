class PacketTypes:
    TIME_SET = 0x01
    TIME_SET_SUCCESS = 0x02
    TIME_SET_FAIL = 0x03
    COLLECTION_DATA = 0x04
    STRING = 0x05
    REQ_CALIBRATION_DATA = 0x06
    HELLO = 0x08
    CALIBRATION_DATA_BMP_280 = 0x09
    LOOP_TIME = 0x0A
    I2C_SCAN_0 = 0x0B
    I2C_SCAN_1 = 0x0C
    SET_BARO_PRESS = 0x0D
    DS_1307_REG_DUMP = 0x0E
    DS_1307_ERASE = 0x0F
    BARO_PRESS_ACK_SUCCESS = 0x10
    BARO_PRESS_ACK_FAIL = 0x11
    GET_BUILD_INFO = 0x12
    W25Q64FV_DEV_INFO = 0x14
    FAULT_DATA = 0x15
    RESTART = 0x16
    NEW_LAUNCH = 0x17
    LAUNCH_DATA = 0x18
    FLUSH_TO_SD_CARD = 0x19
    CALIBRATE_MPU_6050 = 0x1A
    CALIBRATION_DATA_MPU_6050 = 0x1B


packet_lens = {
    PacketTypes.TIME_SET: 8,
    PacketTypes.TIME_SET_SUCCESS: 0,
    PacketTypes.TIME_SET_FAIL: 0,
    PacketTypes.COLLECTION_DATA: 92,
    PacketTypes.STRING: -1,
    PacketTypes.REQ_CALIBRATION_DATA: 0,
    PacketTypes.CALIBRATION_DATA_BMP_280: 34,
    PacketTypes.LOOP_TIME: 24,
    PacketTypes.BARO_PRESS_ACK_SUCCESS: 0,
    PacketTypes.BARO_PRESS_ACK_FAIL: 0,
    PacketTypes.FAULT_DATA: 6,
    PacketTypes.NEW_LAUNCH: 64,
    PacketTypes.LAUNCH_DATA: 88,
    PacketTypes.CALIBRATION_DATA_MPU_6050: 48
}
