from enum import Enum, auto


class FailureType(Enum):
    MODEL = auto()
    TOOL = auto()
    SCHEMA = auto()
    UNKNOWN = auto()
