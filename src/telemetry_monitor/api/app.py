from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from telemetry_monitor.models.telemetry import TelemetryReading
from telemetry_monitor.services.classifier import classify_reading
from telemetry_monitor.storage.database import connect, initialize_database
from telemetry_monitor.storage.repository import TelemetryRepository

app = FastAPI(title="Embedded Telemetry Monitoring System", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BatchTelemetryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source": "api-batch",
                    "readings": [
                        {
                            "device_id": "node-008",
                            "timestamp": "2026-06-24T03:10:00Z",
                            "subsystem": "thermal",
                            "temperature_c": 67.2,
                            "voltage_v": 3.42,
                            "battery_percent": 31.5,
                            "signal_dbm": -82.0,
                            "memory_usage_percent": 76.0,
                            "uptime_seconds": 18500,
                            "packet_sequence": 41,
                        }
                    ],
                }
            ]
        }
    )

    readings: list[TelemetryReading]
    source: str = "api-batch"


def get_repository() -> TelemetryRepository:
    connection = connect()
    initialize_database(connection)
    return TelemetryRepository(connection)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "telemetry-monitor", "version": "0.2.0"}


@app.post("/api/v1/telemetry")
def create_telemetry(
    reading: TelemetryReading,
    repository: TelemetryRepository = Depends(get_repository),
) -> dict:
    classified = classify_reading(reading)
    reading_id = repository.save_reading(classified)
    return {
        "accepted": True,
        "reading_id": reading_id,
        "device_id": classified.device_id,
        "status": classified.status,
        "health_score": classified.health_score,
        "alerts_created": len(classified.active_alerts),
    }


@app.post("/api/v1/telemetry/batch")
def create_telemetry_batch(
    payload: BatchTelemetryRequest,
    repository: TelemetryRepository = Depends(get_repository),
) -> dict:
    accepted = 0
    created_alerts = 0
    reading_ids: list[int] = []
    for reading in payload.readings:
        classified = classify_reading(reading)
        reading_ids.append(repository.save_reading(classified))
        created_alerts += len(classified.active_alerts)
        accepted += 1
    event_id = repository.record_ingestion_event(
        source=payload.source,
        payload_count=len(payload.readings),
        accepted_count=accepted,
        rejected_count=0,
        notes="batch telemetry ingestion",
    )
    return {
        "accepted": accepted,
        "rejected": 0,
        "event_id": event_id,
        "reading_ids": reading_ids,
        "alerts_created": created_alerts,
    }


@app.get("/api/v1/devices")
def list_devices(repository: TelemetryRepository = Depends(get_repository)) -> list[dict]:
    return [device.model_dump() for device in repository.list_devices()]


@app.get("/api/v1/telemetry/latest")
def latest_readings(
    limit: int = Query(default=25, ge=1, le=250),
    repository: TelemetryRepository = Depends(get_repository),
) -> list[dict]:
    return repository.latest_readings(limit=limit)


@app.get("/api/v1/telemetry/history/{device_id}")
def telemetry_history(
    device_id: str,
    limit: int = Query(default=50, ge=1, le=500),
    repository: TelemetryRepository = Depends(get_repository),
) -> list[dict]:
    return repository.readings_for_device(device_id=device_id, limit=limit)


@app.get("/api/v1/alerts")
def list_alerts(
    include_resolved: bool = False,
    limit: int = Query(default=100, ge=1, le=500),
    repository: TelemetryRepository = Depends(get_repository),
) -> list[dict]:
    return repository.list_alerts(include_resolved=include_resolved, limit=limit)


@app.patch("/api/v1/alerts/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    repository: TelemetryRepository = Depends(get_repository),
) -> dict:
    resolved = repository.resolve_alert(alert_id)
    if not resolved:
        raise HTTPException(status_code=404, detail="active alert not found")
    return {"resolved": True, "alert_id": alert_id}


@app.get("/api/v1/summary")
def system_summary(repository: TelemetryRepository = Depends(get_repository)) -> dict:
    return repository.system_summary()
