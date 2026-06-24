from fastapi import FastAPI

app = FastAPI(title="Embedded Telemetry Monitoring System", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
