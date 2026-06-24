from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Alert(BaseModel):
    device_id: str
    severity: str
    metric: str
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: datetime | None = None
    is_resolved: bool = False


class AlertSummary(BaseModel):
    total_active: int
    warning_count: int
    critical_count: int
