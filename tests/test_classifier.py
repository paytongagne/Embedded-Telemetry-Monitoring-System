from telemetry_monitor.models.telemetry import TelemetryReading
from telemetry_monitor.services.classifier import classify_reading


def test_normal_reading_classifies_as_normal() -> None:
    reading = TelemetryReading(
        device_id="node-001",
        subsystem="power",
        temperature_c=40.0,
        voltage_v=3.9,
        battery_percent=75.0,
        signal_dbm=-60.0,
        memory_usage_percent=35.0,
        uptime_seconds=1000,
        packet_sequence=1,
    )

    classified = classify_reading(reading)

    assert classified.status == "NORMAL"
    assert classified.health_score == 100
    assert classified.active_alerts == []


def test_stressed_reading_creates_alerts() -> None:
    reading = TelemetryReading(
        device_id="node-002",
        subsystem="thermal",
        temperature_c=90.0,
        voltage_v=3.0,
        battery_percent=8.0,
        signal_dbm=-105.0,
        memory_usage_percent=95.0,
        uptime_seconds=1200,
        packet_sequence=2,
    )

    classified = classify_reading(reading)

    assert classified.status == "CRITICAL"
    assert classified.health_score < 50
    assert len(classified.active_alerts) >= 3
