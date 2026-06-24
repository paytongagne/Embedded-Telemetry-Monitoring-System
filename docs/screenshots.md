# Demo Screenshots

This page collects the clean screenshots used to show the local FastAPI demo. The screenshots focus on successful endpoints and system behavior instead of default validation-error examples.

## Health Check

The health endpoint confirms that the API service is running and returning the current service version.

![Health endpoint](assets/screenshots/api-health.svg)

## Screenshot Set to Add

The following screenshots were reviewed and are the best ones to include in the repository:

| Screenshot | Purpose | Status |
|---|---|---|
| `api-health.svg` | Shows `/health` returning `200 OK` with service status | Added |
| `api-devices.png` | Shows `/api/v1/devices` returning device health summaries | Add manually |
| `api-latest-telemetry.png` | Shows `/api/v1/telemetry/latest` returning recent classified readings | Add manually |
| `api-alerts.png` | Shows `/api/v1/alerts` returning active warning and critical alerts | Add manually |
| `api-resolve-alert.png` | Shows `PATCH /api/v1/alerts/{alert_id}/resolve` resolving an alert | Add manually |
| `api-summary.png` | Shows `/api/v1/summary` returning fleet-level counts | Add manually |
| `api-schema-contract.png` | Shows OpenAPI schema validation fields for telemetry requests | Add manually |

## Recommended File Location

Place all final screenshots in:

```text
docs/assets/screenshots/
```

Recommended filenames:

```text
api-health.svg
api-devices.png
api-latest-telemetry.png
api-alerts.png
api-resolve-alert.png
api-summary.png
api-schema-contract.png
```

## README Usage

After the image files are added, the README can reference them like this:

```markdown
![Device endpoint](docs/assets/screenshots/api-devices.png)
![Fleet summary endpoint](docs/assets/screenshots/api-summary.png)
```

## Notes

Screenshots that show `422 Unprocessable Entity` from the default Swagger request body should not be used as main project images. Those errors are valid validation behavior, but they are not the strongest first impression for the repository.
