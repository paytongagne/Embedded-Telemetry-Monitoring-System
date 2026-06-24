# Local Deployment

## Local API Run

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
python scripts/seed_demo_data.py
uvicorn telemetry_monitor.api.app:app --reload
```

Open the generated API docs at:

```text
http://127.0.0.1:8000/docs
```

## Makefile Workflow

```bash
make install
make test
make seed
make run-api
```

The Makefile uses the `src` package layout and starts the FastAPI app with the local database in `data/telemetry.db`.

## Dashboard

Start the API, seed demo data, then open:

```text
src/telemetry_monitor/dashboard/index.html
```

The dashboard calls the local API at `http://127.0.0.1:8000` and displays fleet summary cards, device status rows, latest readings, and active alerts.

## Docker Run

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/docs
```

The Docker Compose service mounts a persistent local volume for SQLite data.

## Data Storage

The first version uses SQLite. The database is created automatically in `data/telemetry.db` when the API starts or demo data is seeded.

## Future Deployment Upgrades

- Add PostgreSQL as an optional storage backend
- Add MQTT broker service for publish/subscribe ingestion
- Add dashboard static hosting container
- Add production logging configuration
