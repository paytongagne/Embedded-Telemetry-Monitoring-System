from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from telemetry_monitor.models.device import Device, DeviceSummary
from telemetry_monitor.models.telemetry import ClassifiedTelemetry


class TelemetryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def ping(self) -> bool:
        self.connection.execute("SELECT 1").fetchone()
        return True

    def upsert_device(self, device: Device) -> None:
        self.connection.execute(
            """
            INSERT INTO devices(device_id, name, device_type, firmware_version, location, status, created_at, last_seen_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                name=excluded.name,
                device_type=excluded.device_type,
                firmware_version=excluded.firmware_version,
                location=excluded.location,
                status=excluded.status,
                last_seen_at=excluded.last_seen_at
            """,
            (
                device.device_id,
                device.name,
                device.device_type,
                device.firmware_version,
                device.location,
                device.status,
                device.created_at.isoformat(),
                device.last_seen_at.isoformat() if device.last_seen_at else None,
            ),
        )
        self.connection.commit()

    def save_reading(self, reading: ClassifiedTelemetry) -> int:
        now = datetime.now(timezone.utc).isoformat()
        self.connection.execute(
            """
            INSERT INTO devices(device_id, name, device_type, firmware_version, location, status, created_at, last_seen_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET status=excluded.status, last_seen_at=excluded.last_seen_at
            """,
            (
                reading.device_id,
                reading.device_id,
                "simulated-node",
                "sim-1.0.0",
                "lab",
                reading.status,
                now,
                reading.timestamp.isoformat(),
            ),
        )
        cursor = self.connection.execute(
            """
            INSERT INTO telemetry_readings(
                device_id, timestamp, subsystem, temperature_c, voltage_v, battery_percent,
                signal_dbm, memory_usage_percent, uptime_seconds, packet_sequence,
                health_score, status, active_alerts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reading.device_id,
                reading.timestamp.isoformat(),
                reading.subsystem,
                reading.temperature_c,
                reading.voltage_v,
                reading.battery_percent,
                reading.signal_dbm,
                reading.memory_usage_percent,
                reading.uptime_seconds,
                reading.packet_sequence,
                reading.health_score,
                reading.status,
                json.dumps(reading.active_alerts),
            ),
        )
        reading_id = int(cursor.lastrowid)
        self._create_alert_rows(reading_id, reading, now)
        self.connection.commit()
        return reading_id

    def _create_alert_rows(self, reading_id: int, reading: ClassifiedTelemetry, created_at: str) -> None:
        severity = "CRITICAL" if reading.status == "CRITICAL" else "WARNING"
        if reading.status == "NORMAL":
            return
        for message in reading.active_alerts:
            self.connection.execute(
                """
                INSERT INTO alerts(device_id, reading_id, severity, metric, message, created_at, is_resolved)
                VALUES (?, ?, ?, ?, ?, ?, 0)
                """,
                (reading.device_id, reading_id, severity, self._extract_metric(message), message, created_at),
            )

    @staticmethod
    def _extract_metric(message: str) -> str:
        lowered = message.lower()
        for metric in ("temperature", "voltage", "battery", "signal", "memory"):
            if metric in lowered:
                return metric
        return "system"

    def record_ingestion_event(
        self,
        source: str,
        payload_count: int,
        accepted_count: int,
        rejected_count: int,
        notes: str | None = None,
    ) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO ingestion_events(source, payload_count, accepted_count, rejected_count, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (source, payload_count, accepted_count, rejected_count, notes),
        )
        self.connection.commit()
        return int(cursor.lastrowid)

    def list_devices(self) -> list[DeviceSummary]:
        rows = self.connection.execute(
            """
            SELECT d.device_id, d.status, d.last_seen_at,
                   COALESCE(active_alerts.count, 0) AS active_alerts,
                   latest.health_score AS latest_health_score
            FROM devices d
            LEFT JOIN (
                SELECT device_id, COUNT(*) AS count FROM alerts WHERE is_resolved = 0 GROUP BY device_id
            ) active_alerts ON active_alerts.device_id = d.device_id
            LEFT JOIN (
                SELECT tr.device_id, tr.health_score
                FROM telemetry_readings tr
                INNER JOIN (
                    SELECT device_id, MAX(id) AS id FROM telemetry_readings GROUP BY device_id
                ) latest_ids ON latest_ids.id = tr.id
            ) latest ON latest.device_id = d.device_id
            ORDER BY d.device_id
            """
        ).fetchall()
        return [DeviceSummary(**dict(row)) for row in rows]

    def latest_readings(self, limit: int = 25) -> list[dict]:
        rows = self.connection.execute(
            "SELECT * FROM telemetry_readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

    def readings_for_device(self, device_id: str, limit: int = 50) -> list[dict]:
        rows = self.connection.execute(
            """
            SELECT * FROM telemetry_readings
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (device_id, limit),
        ).fetchall()
        return [dict(row) for row in rows]

    def list_alerts(self, include_resolved: bool = False, limit: int = 100) -> list[dict]:
        if include_resolved:
            rows = self.connection.execute(
                "SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = self.connection.execute(
                "SELECT * FROM alerts WHERE is_resolved = 0 ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def resolve_alert(self, alert_id: int) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        cursor = self.connection.execute(
            """
            UPDATE alerts
            SET is_resolved = 1, resolved_at = ?
            WHERE id = ? AND is_resolved = 0
            """,
            (now, alert_id),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def system_summary(self) -> dict:
        device_counts = self.connection.execute(
            "SELECT status, COUNT(*) AS count FROM devices GROUP BY status"
        ).fetchall()
        status_counts = {row["status"]: row["count"] for row in device_counts}
        active_alerts = self.connection.execute(
            "SELECT COUNT(*) AS count FROM alerts WHERE is_resolved = 0"
        ).fetchone()["count"]
        readings_stored = self.connection.execute(
            "SELECT COUNT(*) AS count FROM telemetry_readings"
        ).fetchone()["count"]
        total_devices = sum(status_counts.values())
        return {
            "total_devices": total_devices,
            "normal_devices": status_counts.get("NORMAL", 0),
            "warning_devices": status_counts.get("WARNING", 0),
            "critical_devices": status_counts.get("CRITICAL", 0),
            "offline_devices": status_counts.get("OFFLINE", 0),
            "active_alerts": active_alerts,
            "readings_stored": readings_stored,
        }
