# Windows Setup Notes

These commands assume PowerShell on Windows.

## Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Install project

```powershell
pip install -e ".[dev]"
```

## Seed demo data

```powershell
python scripts/seed_demo_data.py
```

## Start API

```powershell
uvicorn telemetry_monitor.api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```powershell
pytest
```

## Open dashboard

After the API is running, open this file in a browser:

```text
src/telemetry_monitor/dashboard/index.html
```
