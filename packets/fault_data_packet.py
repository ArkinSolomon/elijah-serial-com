import payload_state


class FaultDataPacket:
    device_status: int
    fault_bmp_180: bool
    fault_ds_1307: bool
    fault_i2c_bus0: bool
    fault_bmp_280: bool
    fault_hmc_5883l: bool
    fault_mpu_6050: bool
    fault_i2c_bus1: bool
    fault_w25q64fv: bool


    def __init__(self, data: bytearray):
        self.device_status = data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3]
        self.fault_bmp_180 = data[4] & 0x80 > 0
        self.fault_ds_1307 = data[4] & 0x40 > 0
        self.fault_i2c_bus0 = data[4] & 0x20 > 0
        self.fault_bmp_280 = data[4] & 0x10 > 0
        self.fault_hmc_5883l = data[4] & 0x08 > 0
        self.fault_mpu_6050 = data[4] & 0x04 > 0
        self.fault_i2c_bus1 = data[4] & 0x10 > 0
        self.fault_w25q64fv = data[4] & 0x08 > 0

    def update_payload_state(self):
        payload_state.last_fault_data = self