import json
from pathlib import Path

from telemetry_monitor.services.classifier import classify_reading
from telemetry_monitor.services.simulator import TelemetrySimulator


simulator = TelemetrySimulator(seed=42)
readings = simulator.fleet_snapshot(device_count=8, mode="mixed")
output_path = Path("sample_data/generated_readings.jsonl")
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as file:
    for reading in readings:
        file.write(json.dumps(classify_reading(reading).model_dump(mode="json")) + "\n")

print(f"wrote {len(readings)} readings to {output_path}")
