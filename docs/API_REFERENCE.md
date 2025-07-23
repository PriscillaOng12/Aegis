# API Reference – Aegis Health

This document describes the REST and WebSocket endpoints exposed by the FastAPI service. All endpoints are versioned under `/v1`. Authentication via OAuth2 bearer token is required unless specified.

## Authentication

Clients authenticate using OAuth2 with PKCE. Exchange an Auth0 code for a JWT by calling `/v1/auth/exchange`:

```
POST /v1/auth/exchange
Content-Type: application/json

{
  "auth_code": "abc123",
  "code_verifier": "randomstring"
}
```

**Response**

```
200 OK
{
  "access_token": "eyJhbGci...",
  "expires_in": 3600,
  "refresh_token": "...
}
```

## Symptom Logging

Log a symptom entry with free text and severity sliders:

```
POST /v1/symptoms
Authorization: Bearer <token>
Content-Type: application/json

{
  "pain": 5,
  "fatigue": 3,
  "nausea": 0,
  "notes": "sharp joint pain in the morning",
  "timestamp": "2025-08-10T07:30:00Z"
}
```

**Response**

```
201 Created
{
  "id": "0e8e0f0c-5eb5-4d10-b78d-67cd7e7c7a60",
  "user_id": "aad3...",
  "created_at": "2025-08-10T07:30:05Z"
}
```

## Risk Score

Fetch the latest risk for the current user. Returns a risk percentage, top feature drivers and estimated lead time.

```
GET /v1/risk/latest
Authorization: Bearer <token>

200 OK
{
  "risk_percentage": 0.32,
  "top_drivers": [
    {"feature": "sleep_efficiency_mean_7d", "impact": 0.12},
    {"feature": "pain", "impact": 0.08},
    {"feature": "hrv_rmssd_mean_3d", "impact": 0.05}
  ],
  "lead_time_hours": 18.4
}
```

### Streaming updates

Subscribe to live risk updates via WebSocket:

```
GET /v1/risk/stream
Sec-WebSocket-Protocol: bearer,
Authorization: Bearer <token>

// On message
{
  "timestamp": "2025-08-10T08:00:00Z",
  "risk_percentage": 0.35
}
```

## Wearables Sync

Upload a batch of wearable snapshots (mock or real). The server stores raw data and publishes events for feature extraction.

```
POST /v1/wearables/sync
Authorization: Bearer <token>
Content-Type: application/json

{
  "source": "apple_health",
  "snapshots": [
    {"timestamp": "2025-08-10T06:00:00Z", "hr": 62, "hrv": 50, "steps": 123, "sleep": 0},
    {"timestamp": "2025-08-10T06:05:00Z", "hr": 63, "hrv": 52, "steps": 126, "sleep": 0}
  ]
}
```

**Response**

```
202 Accepted
{
  "ingested": 2
}
```

## Interventions

Trigger an intervention (nudge) manually or via automation. Useful for experiments.

```
POST /v1/interventions/trigger
Authorization: Bearer <token>
Content-Type: application/json

{
  "template_id": "nudge_hydration",
  "user_id": "aad3...",
  "scheduled_for": "2025-08-10T09:00:00Z"
}
```

**Response**

```
202 Accepted
{
  "intervention_id": "2b3c..."
}
```

## Analytics Summary

Return aggregated metrics for the clinician’s cohort (requires `clinician` role):

```
GET /v1/analytics/summary
Authorization: Bearer <token>

200 OK
{
  "adherence": 0.67,
  "false_alert_rate": 0.21,
  "median_lead_time_hours": 14.2,
  "active_users": 125
}
```

## OpenAPI Specification

An up‑to‑date OpenAPI schema is located at [`api/openapi.json`](../api/openapi.json). Generate a new version by running `make openapi`.
