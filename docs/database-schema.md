# Database Schema

The local development database uses SQLite. The schema is intentionally relational so the project can later move to PostgreSQL without changing the overall model.

## `devices`

Stores the latest known state for each simulated device.

| Column | Purpose |
|---|---|
| `device_id` | Stable unique device identifier |
| `name` | Human-readable device name |
| `device_type` | Device category |
| `firmware_version` | Firmware or simulator version |
| `location` | Logical location |
| `status` | Latest health state |
| `created_at` | First time the device was registered |
| `last_seen_at` | Latest telemetry timestamp |

## `telemetry_readings`

Stores each classified reading.

Key fields include device ID, timestamp, subsystem, temperature, voltage, battery level, signal strength, memory usage, uptime, packet sequence, health score, and status.

## `alerts`

Stores alert records created from unhealthy readings. The first version stores alert text in the classified reading, while the schema leaves room for a fuller alert lifecycle.

## Indexes

The schema adds indexes for common queries:

- readings by device and time
- active alerts by device
