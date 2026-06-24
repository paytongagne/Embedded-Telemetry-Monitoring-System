# Embedded Telemetry Monitoring System

A Python-based backend system for monitoring simulated embedded-device telemetry. The project models a realistic device data pipeline: simulated readings are validated, classified by health state, stored in SQLite, and exposed through FastAPI endpoints.

The system is structured around backend service design, database persistence, API workflows, automated testing, dashboard integration, and embedded-style data modeling.

## Features

- Simulated multi-device telemetry generation
- Pydantic data validation for incoming readings
- Health classification for normal, warning, and critical states
- SQLite schema for devices, telemetry readings, alerts, and ingestion events
- Repository layer for storing and querying telemetry data
- FastAPI endpoints for telemetry ingestion, batch ingestion, device summaries, alerts, history, and fleet summaries
- Health, readiness, and version endpoints
- Request timing header and request logging middleware
- Environment-based runtime configuration
- SQLite foreign key enforcement, busy timeout, and optional WAL mode
- Local dashboard for viewing device status, recent readings, and active alerts
- Unit and API integration tests
- Makefile commands for local development
- Docker and Docker Compose support
- Architecture, API, database, deployment, demo, and production-readiness documentation

## System Flow

```text
Device Simulator -> Telemetry Model -> Health Classifier -> SQLite Storage -> FastAPI -> Dashboard/API Client
```

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- Pydantic Settings
- SQLite
- Pytest
- Ruff
- Docker Compose
- HTML/CSS/JavaScript dashboard

## Project Structure

```text
src/telemetry_monitor/
  api/          FastAPI app
  core/         configuration, status definitions, and logging setup
  models/       telemetry, device, and alert models
  services/     simulator and classification logic
  storage/      SQLite schema and repository layer
  dashboard/    local fleet health dashboard
scripts/        demo and seed-data helpers
sample_data/    example telemetry payloads
tests/          automated tests
docs/           architecture and API documentation
```

## Quick Demo

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e ".[dev]"
python scripts/seed_demo_data.py
uvicorn telemetry_monitor.api.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

The dashboard shell is located at:

```text
src/telemetry_monitor/dashboard/index.html
```

## Runtime Configuration

Copy `.env.example` to `.env` and adjust values as needed.

```text
APP_ENV=local
DATABASE_PATH=data/telemetry.db
LOG_LEVEL=INFO
ENABLE_SQLITE_WAL=true
API_HOST=127.0.0.1
API_PORT=8000
```

## API Demo Captures

The local FastAPI demo has been tested with successful responses for:

| Endpoint | What it shows |
|---|---|
| `GET /health` | Service process status and version |
| `GET /ready` | Database readiness check |
| `GET /version` | Service version and runtime environment |
| `GET /api/v1/devices` | Device summaries, latest status, health score, and alert count |
| `GET /api/v1/telemetry/latest` | Recent classified telemetry readings |
| `GET /api/v1/alerts` | Active warning and critical alerts |
| `PATCH /api/v1/alerts/{alert_id}/resolve` | Alert resolution workflow |
| `GET /api/v1/summary` | Fleet-level counts for devices, alerts, and stored readings |

Demo capture documentation is available in [Demo Captures](docs/screenshots.md).

## Makefile Workflow

```bash
make install
make test
make seed
make run-api
```

## Docker Run

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example Telemetry Payload

```json
{
  "device_id": "node-001",
  "timestamp": "2026-06-24T03:05:00Z",
  "subsystem": "power",
  "temperature_c": 42.5,
  "voltage_v": 3.8,
  "battery_percent": 76.2,
  "signal_dbm": -62.0,
  "memory_usage_percent": 44.1,
  "uptime_seconds": 8421,
  "packet_sequence": 12
}
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/ready` | Database readiness check |
| GET | `/version` | Service version and runtime metadata |
| POST | `/api/v1/telemetry` | Submit one telemetry reading |
| POST | `/api/v1/telemetry/batch` | Submit a batch of telemetry readings |
| GET | `/api/v1/devices` | List device status summaries |
| GET | `/api/v1/telemetry/latest` | Read latest stored telemetry records |
| GET | `/api/v1/telemetry/history/{device_id}` | Read recent telemetry for one device |
| GET | `/api/v1/alerts` | List active or resolved alerts |
| PATCH | `/api/v1/alerts/{alert_id}/resolve` | Resolve an active alert |
| GET | `/api/v1/summary` | Read fleet-level device and alert totals |

## Roadmap

- Add dashboard charts for telemetry trends
- Add MQTT-style ingestion service
- Add PostgreSQL option
- Add ESP32 payload example
- Add API key protection for write endpoints
- Add structured JSON logs and metrics counters

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Database Schema](docs/database-schema.md)
- [Deployment](docs/deployment.md)
- [Demo Guide](docs/demo-guide.md)
- [Demo Captures](docs/screenshots.md)
- [System Design](docs/system-design.md)
- [Production Readiness](docs/production-readiness.md)
