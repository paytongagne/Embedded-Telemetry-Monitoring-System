from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Device(BaseModel):
    device_id: str = Field(min_length=3, max_length=80)
    name: str
    device_type: str = "simulated-node"
    firmware_version: str = "sim-1.0.0"
    location: str = "lab"
    status: str = "UNKNOWN"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen_at: datetime | None = None


class DeviceSummary(BaseModel):
    device_id: str
    status: str
    last_seen_at: datetime | None
    active_alerts: int
    latest_health_score: int | None = None
