from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogMessage:
    message: str
    timestamp: datetime
    is_system: bool

    def __init__(self, message: str, is_system = False):
        self.message = message
        self.timestamp = datetime.now()
        self.is_system = is_system

    def __str__(self):
        return f'[{self.get_formatted_timestamp()}]{'[SYSTEM]' if self.is_system else ''} {self.message}'

    def get_formatted_timestamp(self):
        return self.timestamp.strftime(r'%I:%M:%S')