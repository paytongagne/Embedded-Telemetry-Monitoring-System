from fastapi import Depends, FastAPI

from telemetry_monitor.models.telemetry import TelemetryReading
from telemetry_monitor.services.classifier import classify_reading
from telemetry_monitor.storage.database import connect, initialize_database
from telemetry_monitor.storage.repository import TelemetryRepository

app = FastAPI(title="Embedded Telemetry Monitoring System", version="0.1.0")


def get_repository() -> TelemetryRepository:
    connection = connect()
    initialize_database(connection)
    return TelemetryRepository(connection)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


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


@app.get("/api/v1/devices")
def list_devices(repository: TelemetryRepository = Depends(get_repository)) -> list[dict]:
    return [device.model_dump() for device in repository.list_devices()]


@app.get("/api/v1/telemetry/latest")
def latest_readings(
    limit: int = 25,
    repository: TelemetryRepository = Depends(get_repository),
) -> list[dict]:
    return repository.latest_readings(limit=limit)
