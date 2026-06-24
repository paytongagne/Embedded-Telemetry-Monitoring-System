# System Architecture

The Embedded Telemetry Monitoring System is organized as a layered backend system for simulated connected-device health monitoring.

```text
Simulated Device Fleet
        |
        v
Telemetry Reading Model
        |
        v
Health Classification Service
        |
        v
SQLite Repository Layer
        |
        v
FastAPI Endpoints
        |
        v
Dashboard / API Consumers
```

## Components

### Device Simulator
Generates realistic readings for multiple simulated nodes. Each reading includes temperature, voltage, battery level, signal strength, memory usage, uptime, subsystem, and packet sequence.

### Telemetry Model
Defines the required payload format and validates incoming readings before they are classified or stored.

### Classification Service
Scores each reading and assigns a health state. Readings can be normal, warning, or critical depending on metric ranges.

### Storage Layer
Uses SQLite for local development. The schema tracks devices, telemetry readings, and alerts while keeping the design easy to migrate to PostgreSQL later.

### API Layer
FastAPI exposes health checks, telemetry ingestion, device summaries, and latest readings.

## Design Goals

- Keep local setup simple.
- Make the project understandable to recruiters.
- Show backend, database, testing, and embedded-style data skills.
- Leave a clear path for MQTT, Docker, and dashboard expansion.
