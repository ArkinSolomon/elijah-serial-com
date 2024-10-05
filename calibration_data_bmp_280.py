class CalibrationDataBMP280:
    dig_T1: int
    dig_T2: int
    dig_T3: int
    dig_P1: int
    dig_P2: int
    dig_P3: int
    dig_P4: int
    dig_P5: int
    dig_P6: int
    dig_P7: int
    dig_P8: int
    dig_P9: int
    sea_level_pressure: float

    def __str__(self):
        return f"T1: {self.dig_T1} T2: {self.dig_T2} T3: {self.dig_T3} P1: {self.dig_P1} P2: {self.dig_P2} P3: {self.dig_P3} P4: {self.dig_P4} P5: {self.dig_P5} P6: {self.dig_P6} P7: {self.dig_P7} P8: {self.dig_P8} P9: {self.dig_P9} Sea Level Pressure: {self.sea_level_pressure}"