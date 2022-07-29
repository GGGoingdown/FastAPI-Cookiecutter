from enum import Enum


class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEUBG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Environment Mode
class EnvironmentMode(str, Enum):
    DEV = "DEV"
    TEST = "TEST"
    STAG = "STAG"
    PROD = "PROD"
