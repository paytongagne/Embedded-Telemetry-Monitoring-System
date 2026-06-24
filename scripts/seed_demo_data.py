from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from telemetry_monitor.services.classifier import classify_reading
from telemetry_monitor.services.simulator import TelemetrySimulator
from telemetry_monitor.storage.database import connect, initialize_database
from telemetry_monitor.storage.repository import TelemetryRepository

DATA_DIR = ROOT / "data"
SAMPLE_DIR = ROOT / "sample_data"
DB_PATH = DATA_DIR / "telemetry.db"


def seed_demo_data(rounds: int = 40, device_count: int = 6) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    SAMPLE_DIR.mkdir(exist_ok=True)
    connection = connect(str(DB_PATH))
    initialize_database(connection)
    repository = TelemetryRepository(connection)
    simulator = TelemetrySimulator(seed=42)

    modes = ["normal", "normal", "warning", "critical"]
    stored = 0
    alert_count = 0
    mixed_path = SAMPLE_DIR / "mixed_fleet_readings.jsonl"

    with mixed_path.open("w", encoding="utf-8") as output:
        for round_index in range(rounds):
            mode = modes[round_index % len(modes)]
            readings = simulator.fleet_snapshot(device_count=device_count, mode=mode)
            for reading in readings:
                classified = classify_reading(reading)
                repository.save_reading(classified)
                output.write(json.dumps(reading.model_dump(mode="json")) + "\n")
                stored += 1
                alert_count += len(classified.active_alerts)

    repository.record_ingestion_event(
        source="seed-demo-data",
        payload_count=stored,
        accepted_count=stored,
        rejected_count=0,
        notes="generated local demo dataset",
    )
    return {
        "database": str(DB_PATH),
        "sample_file": str(mixed_path),
        "readings_stored": stored,
        "alerts_created": alert_count,
    }


if __name__ == "__main__":
    result = seed_demo_data()
    print("Demo data seeded")
    for key, value in result.items():
        print(f"{key}: {value}")
