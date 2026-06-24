# API Reference

The API is implemented with FastAPI and is designed around simple JSON telemetry workflows.

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Submit Telemetry

```http
POST /api/v1/telemetry
```

Request body:

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

Response:

```json
{
  "accepted": true,
  "reading_id": 1,
  "device_id": "node-001",
  "status": "NORMAL",
  "health_score": 100,
  "alerts_created": 0
}
```

## List Devices

```http
GET /api/v1/devices
```

Returns device status summaries.

## Latest Readings

```http
GET /api/v1/telemetry/latest?limit=25
```

Returns the latest stored telemetry records.
