class CalibrationData:
    AC1: int
    AC2: int
    AC3: int
    AC4: int
    AC5: int
    AC6: int
    B1: int
    B2: int
    MB: int
    MC: int
    MD: int

    def __str__(self):
        return f"AC1: {self.AC1}, AC2: {self.AC2}, AC3: {self.AC3}, AC4: {self.AC4}, AC5: {self.AC5}, AC6: {self.AC6}, B1: {self.B1}, B2: {self.B2}, MB: {self.MB}, MC: {self.MC}, MD: {self.MD}"
