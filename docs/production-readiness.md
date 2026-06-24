# Production Readiness Notes

This document tracks operational design choices for running the telemetry service outside a one-off local demo.

## Runtime Configuration

Runtime settings are loaded from environment variables through `pydantic-settings`.

Supported variables:

| Variable | Purpose |
|---|---|
| `APP_ENV` | Runtime environment label such as `local`, `test`, or `production` |
| `DATABASE_PATH` | SQLite database path |
| `LOG_LEVEL` | Python logging level |
| `ENABLE_SQLITE_WAL` | Enables SQLite write-ahead logging for local concurrent reads/writes |
| `API_HOST` | Local API host used by helper commands |
| `API_PORT` | Local API port used by helper commands |

## Health and Readiness

The service exposes separate checks:

| Endpoint | Purpose |
|---|---|
| `/health` | Confirms the FastAPI process is running |
| `/ready` | Confirms the application can reach the database layer |
| `/version` | Returns service version and environment metadata |

## Request Logging

The API includes request logging middleware that records method, path, response status, and request duration. Each response also includes an `X-Process-Time-ms` header.

## Database Settings

The SQLite connection enables:

- Foreign key enforcement
- Busy timeout handling
- Optional write-ahead logging

SQLite is appropriate for the local demo and lightweight testing path. A PostgreSQL adapter is the next production-focused storage upgrade.

## CI Checks

GitHub Actions installs the package, runs tests, and runs Ruff linting. The integration tests exercise ingestion, device listing, history, summary, alert creation, alert resolution, health, readiness, and version endpoints.

## Next Operational Upgrades

- PostgreSQL storage backend
- Structured JSON logs
- API key authentication for write endpoints
- Rate limiting for ingestion endpoints
- Metrics endpoint for counters and request latency
- Container healthcheck wired to `/ready`
