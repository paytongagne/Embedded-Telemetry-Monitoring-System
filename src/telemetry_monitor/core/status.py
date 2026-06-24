from enum import StrEnum


class HealthState(StrEnum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"


SUBSYSTEMS = {"power", "thermal", "comms", "compute"}
