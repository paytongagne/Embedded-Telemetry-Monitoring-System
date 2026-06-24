# Local Deployment

## Local API Run

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn telemetry_monitor.api.app:app --reload
```

Open the generated API docs at:

```text
http://127.0.0.1:8000/docs
```

## Data Storage

The first version uses a local SQLite database named `telemetry.db`. The database is created automatically when the API starts and the repository initializes the schema.

## Environment Plan

Future versions should move runtime settings into environment variables:

```text
TELEMETRY_DATABASE_PATH=telemetry.db
TELEMETRY_API_HOST=127.0.0.1
TELEMETRY_API_PORT=8000
```

## Future Docker Plan

The next deployment upgrade should include:

- API container
- database container
- optional MQTT broker container
- mounted sample data volume
