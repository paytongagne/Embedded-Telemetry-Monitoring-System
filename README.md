# Embedded Telemetry Monitoring System

A Python-based backend system for monitoring simulated embedded-device telemetry. The project models a realistic device data pipeline: simulated readings are validated, classified by health state, stored in SQLite, and exposed through FastAPI endpoints.

This repo is designed as a workplace-ready portfolio project showing backend development, database design, API workflows, automated testing, and embedded-style data modeling.

## Features

- Simulated multi-device telemetry generation
- Pydantic data validation for incoming readings
- Health classification for normal, warning, and critical states
- SQLite schema for devices, telemetry readings, and alerts
- Repository layer for storing and querying telemetry data
- FastAPI endpoints for ingestion, device summaries, and latest readings
- Unit tests for classification behavior
- Architecture, API, and database documentation

## System Flow

```text
Device Simulator -> Telemetry Model -> Health Classifier -> SQLite Storage -> FastAPI -> Dashboard/API Client
```

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLite
- Pytest
- Ruff

## Project Structure

```text
src/telemetry_monitor/
  api/          FastAPI app
  core/         shared status definitions
  models/       telemetry, device, and alert models
  services/     simulator and classification logic
  storage/      SQLite schema and repository layer
scripts/        helper scripts for sample data
tests/          automated tests
docs/           architecture and API documentation
```

## Quick Start

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn telemetry_monitor.api.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example Telemetry Payload

```json
{
  "device_id": "node-001",
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
| POST | `/api/v1/telemetry` | Submit one telemetry reading |
| GET | `/api/v1/devices` | List device status summaries |
| GET | `/api/v1/telemetry/latest` | Read latest stored telemetry records |

## Resume Relevance

This project demonstrates the ability to build software that connects device-style data, validation logic, backend APIs, database persistence, and technical documentation.

Resume-safe bullet:

> Built an embedded telemetry monitoring system using Python, FastAPI, Pydantic, and SQLite to simulate connected-device health tracking, classify telemetry status, persist readings, and expose backend API endpoints.

## Roadmap

- Add dashboard UI that consumes the API
- Add MQTT-style ingestion service
- Add Docker Compose setup
- Add PostgreSQL option
- Add API integration tests
- Add GitHub Actions workflow
- Add dashboard screenshots and demo data

## Documentation

- [Architecture](docs/architecture.md)
- [API Reference](docs/api-reference.md)
- [Database Schema](docs/database-schema.md)
- [System Design](docs/system-design.md)
