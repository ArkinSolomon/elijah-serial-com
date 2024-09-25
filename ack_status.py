from enum import Enum


class AckStatus(Enum):
    NOT_WAITING = 0
    WAITING = 1
    SUCCESS = 2
    FAILED = 3

    @staticmethod
    def to_string(status: 'AckStatus'):
        match status:
            case AckStatus.NOT_WAITING:
                return 'NOT_WAITING'
            case AckStatus.WAITING:
                return 'WAITING'
            case AckStatus.SUCCESS:
                return 'SUCCESS'
            case AckStatus.FAILED:
                return 'FAILED'