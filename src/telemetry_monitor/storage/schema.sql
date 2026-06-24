CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    device_type TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_seen_at TEXT
);

CREATE TABLE IF NOT EXISTS telemetry_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    subsystem TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    voltage_v REAL NOT NULL,
    battery_percent REAL NOT NULL,
    signal_dbm REAL NOT NULL,
    memory_usage_percent REAL NOT NULL,
    uptime_seconds INTEGER NOT NULL,
    packet_sequence INTEGER NOT NULL,
    health_score INTEGER NOT NULL,
    status TEXT NOT NULL,
    active_alerts TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    reading_id INTEGER,
    severity TEXT NOT NULL,
    metric TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    is_resolved INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (reading_id) REFERENCES telemetry_readings(id)
);

CREATE TABLE IF NOT EXISTS ingestion_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    payload_count INTEGER NOT NULL,
    accepted_count INTEGER NOT NULL,
    rejected_count INTEGER NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_readings_device_time ON telemetry_readings(device_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_readings_status ON telemetry_readings(status);
CREATE INDEX IF NOT EXISTS idx_alerts_device_active ON alerts(device_id, is_resolved);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity, is_resolved);
