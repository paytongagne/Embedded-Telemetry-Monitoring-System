from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Subsystem = Literal["power", "thermal", "comms", "compute"]


class TelemetryReading(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "device_id": "node-007",
                    "timestamp": "2026-06-24T03:05:00Z",
                    "subsystem": "power",
                    "temperature_c": 42.5,
                    "voltage_v": 3.75,
                    "battery_percent": 82.0,
                    "signal_dbm": -64.0,
                    "memory_usage_percent": 41.0,
                    "uptime_seconds": 12000,
                    "packet_sequence": 1,
                }
            ]
        }
    )

    device_id: str = Field(min_length=3, max_length=80)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    subsystem: Subsystem
    temperature_c: float
    voltage_v: float
    battery_percent: float = Field(ge=0.0, le=100.0)
    signal_dbm: float
    memory_usage_percent: float = Field(ge=0.0, le=100.0)
    uptime_seconds: int = Field(ge=0)
    packet_sequence: int = Field(ge=0)

    @field_validator("voltage_v")
    @classmethod
    def voltage_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("voltage_v must be positive")
        return value


class ClassifiedTelemetry(TelemetryReading):
    status: str
    health_score: int
    active_alerts: list[str] = Field(default_factory=list)
