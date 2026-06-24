from __future__ import annotations

from fastapi.testclient import TestClient

from telemetry_monitor.api.app import app, get_repository
from telemetry_monitor.storage.database import initialize_database
from telemetry_monitor.storage.repository import TelemetryRepository


def test_api_ingestion_summary_and_alert_flow(tmp_path):
    database_path = tmp_path / "test-telemetry.db"

    def override_repository() -> TelemetryRepository:
        import sqlite3

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        initialize_database(connection)
        return TelemetryRepository(connection)

    app.dependency_overrides[get_repository] = override_repository
    client = TestClient(app)

    normal_payload = {
        "device_id": "node-001",
        "subsystem": "power",
        "temperature_c": 40.0,
        "voltage_v": 3.8,
        "battery_percent": 88.0,
        "signal_dbm": -62.0,
        "memory_usage_percent": 35.0,
        "uptime_seconds": 5000,
        "packet_sequence": 1,
    }
    critical_payload = {
        "device_id": "node-002",
        "subsystem": "thermal",
        "temperature_c": 93.0,
        "voltage_v": 2.9,
        "battery_percent": 6.0,
        "signal_dbm": -105.0,
        "memory_usage_percent": 96.0,
        "uptime_seconds": 8000,
        "packet_sequence": 1,
    }

    assert client.get("/health").status_code == 200

    normal_response = client.post("/api/v1/telemetry", json=normal_payload)
    assert normal_response.status_code == 200
    assert normal_response.json()["status"] == "NORMAL"

    critical_response = client.post("/api/v1/telemetry", json=critical_payload)
    assert critical_response.status_code == 200
    assert critical_response.json()["status"] == "CRITICAL"
    assert critical_response.json()["alerts_created"] >= 1

    devices = client.get("/api/v1/devices").json()
    assert len(devices) == 2

    latest = client.get("/api/v1/telemetry/latest?limit=2").json()
    assert len(latest) == 2

    history = client.get("/api/v1/telemetry/history/node-002?limit=5").json()
    assert len(history) == 1
    assert history[0]["status"] == "CRITICAL"

    alerts = client.get("/api/v1/alerts").json()
    assert len(alerts) >= 1

    summary = client.get("/api/v1/summary").json()
    assert summary["total_devices"] == 2
    assert summary["critical_devices"] == 1
    assert summary["readings_stored"] == 2
    assert summary["active_alerts"] >= 1

    alert_id = alerts[0]["id"]
    resolve_response = client.patch(f"/api/v1/alerts/{alert_id}/resolve")
    assert resolve_response.status_code == 200
    assert resolve_response.json()["resolved"] is True

    app.dependency_overrides.clear()
