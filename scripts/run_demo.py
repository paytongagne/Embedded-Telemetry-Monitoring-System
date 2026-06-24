from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from seed_demo_data import seed_demo_data


def main() -> None:
    result = seed_demo_data(rounds=20, device_count=5)
    print("\nEmbedded Telemetry Monitoring System demo is ready.")
    print(f"Database: {result['database']}")
    print(f"Seeded readings: {result['readings_stored']}")
    print(f"Alerts created: {result['alerts_created']}")
    print("\nRun the API:")
    print("  uvicorn telemetry_monitor.api.app:app --reload")
    print("\nOpen API docs:")
    print("  http://127.0.0.1:8000/docs")
    print("\nOpen dashboard:")
    print("  src/telemetry_monitor/dashboard/index.html")


if __name__ == "__main__":
    main()
