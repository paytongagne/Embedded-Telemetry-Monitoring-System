# Demo Guide

This guide walks through the local demo flow for the telemetry monitoring system.

## 1. Install dependencies

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e ".[dev]"
```

## 2. Seed demo data

```bash
python scripts/seed_demo_data.py
```

This creates a local SQLite database in `data/telemetry.db` and writes generated telemetry samples to `sample_data/mixed_fleet_readings.jsonl`.

## 3. Start the API

```bash
uvicorn telemetry_monitor.api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 4. Inspect core endpoints

Use the API docs to try:

```text
GET /health
GET /api/v1/summary
GET /api/v1/devices
GET /api/v1/telemetry/latest
GET /api/v1/alerts
GET /api/v1/telemetry/history/node-001
```

## 5. Open dashboard

Open the dashboard file in a browser:

```text
src/telemetry_monitor/dashboard/index.html
```

The dashboard expects the API to be running at `http://127.0.0.1:8000`.

## Makefile option

```bash
make install
make seed
make run-api
```

## Demo checklist

- API health check returns `ok`
- Summary endpoint shows stored devices and readings
- Devices endpoint shows normal, warning, or critical statuses
- Alerts endpoint shows generated warning or critical records
- Dashboard loads summary cards and status tables
- API integration tests pass with `make test`
