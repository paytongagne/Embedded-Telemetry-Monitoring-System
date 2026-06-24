# Demo Screenshots

This page tracks the clean screenshots used to show the local FastAPI demo. The screenshots should focus on successful endpoints and system behavior instead of default validation-error examples.

## Current Screenshot Status

| Screenshot | Purpose | Status |
|---|---|---|
| `api-health.png` | Shows `/health` returning `200 OK` with service status | Capture manually |
| `api-devices.png` | Shows `/api/v1/devices` returning device health summaries | Capture manually |
| `api-latest-telemetry.png` | Shows `/api/v1/telemetry/latest` returning classified readings | Capture manually |
| `api-alerts.png` | Shows `/api/v1/alerts` returning active warning and critical alerts | Capture manually |
| `api-resolve-alert.png` | Shows `PATCH /api/v1/alerts/{alert_id}/resolve` resolving an alert | Capture manually |
| `api-summary.png` | Shows `/api/v1/summary` returning fleet-level counts | Capture manually |
| `api-schema-contract.png` | Shows OpenAPI schema validation fields for telemetry requests | Capture manually |

## Recommended File Location

Place final screenshots in:

```text
docs/assets/screenshots/
```

Recommended filenames:

```text
api-health.png
api-devices.png
api-latest-telemetry.png
api-alerts.png
api-resolve-alert.png
api-summary.png
api-schema-contract.png
```

## Recommended README Usage

After the image files are uploaded, the README can reference them like this:

```markdown
![Device endpoint](docs/assets/screenshots/api-devices.png)
![Fleet summary endpoint](docs/assets/screenshots/api-summary.png)
```

## Capture Guidance

Use screenshots that show a successful `200` response when possible. The best screenshots from the current demo are:

- `GET /health`
- `GET /api/v1/devices`
- `GET /api/v1/telemetry/latest`
- `GET /api/v1/alerts`
- `PATCH /api/v1/alerts/{alert_id}/resolve`
- `GET /api/v1/summary`
- OpenAPI schema view for telemetry request fields

## Notes

Screenshots that show `422 Unprocessable Entity` from the default Swagger request body should not be used as main project images. Those errors are valid validation behavior, but they are not the strongest first impression for the repository.

The old SVG test asset was removed from the README because it rendered as a broken placeholder in GitHub. Use normal PNG screenshots for final repository images.
