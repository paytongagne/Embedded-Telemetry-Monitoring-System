from __future__ import annotations

import random
from datetime import datetime, timezone

from telemetry_monitor.models.telemetry import TelemetryReading


class TelemetrySimulator:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)
        self.sequence_by_device: dict[str, int] = {}

    def next_reading(self, device_id: str, subsystem: str = "power", mode: str = "normal") -> TelemetryReading:
        sequence = self.sequence_by_device.get(device_id, 0) + 1
        self.sequence_by_device[device_id] = sequence

        profile = self._profile(mode)
        return TelemetryReading(
            device_id=device_id,
            timestamp=datetime.now(timezone.utc),
            subsystem=subsystem,  # type: ignore[arg-type]
            temperature_c=self.random.uniform(*profile["temperature_c"]),
            voltage_v=self.random.uniform(*profile["voltage_v"]),
            battery_percent=self.random.uniform(*profile["battery_percent"]),
            signal_dbm=self.random.uniform(*profile["signal_dbm"]),
            memory_usage_percent=self.random.uniform(*profile["memory_usage_percent"]),
            uptime_seconds=self.random.randint(60, 2_000_000),
            packet_sequence=sequence,
        )

    def fleet_snapshot(self, device_count: int = 5, mode: str = "mixed") -> list[TelemetryReading]:
        readings: list[TelemetryReading] = []
        modes = ["normal", "normal", "warning", "critical"] if mode == "mixed" else [mode]
        subsystems = ["power", "thermal", "comms", "compute"]
        for index in range(device_count):
            readings.append(
                self.next_reading(
                    device_id=f"node-{index + 1:03d}",
                    subsystem=self.random.choice(subsystems),
                    mode=self.random.choice(modes),
                )
            )
        return readings

    def _profile(self, mode: str) -> dict[str, tuple[float, float]]:
        if mode == "critical":
            return {
                "temperature_c": (82.0, 96.0),
                "voltage_v": (2.8, 3.25),
                "battery_percent": (3.0, 14.0),
                "signal_dbm": (-108.0, -92.0),
                "memory_usage_percent": (88.0, 98.0),
            }
        if mode == "warning":
            return {
                "temperature_c": (65.0, 78.0),
                "voltage_v": (3.15, 3.55),
                "battery_percent": (14.0, 32.0),
                "signal_dbm": (-94.0, -78.0),
                "memory_usage_percent": (74.0, 88.0),
            }
        return {
            "temperature_c": (28.0, 55.0),
            "voltage_v": (3.55, 4.15),
            "battery_percent": (45.0, 99.0),
            "signal_dbm": (-76.0, -45.0),
            "memory_usage_percent": (18.0, 68.0),
        }
