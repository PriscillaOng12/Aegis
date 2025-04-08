# ADR 0001 – Overall Architecture

## Status

Accepted – 2025‑08‑10

## Context

We needed to design an architecture that supports:

* **Real‑time risk scoring** for patients using heterogeneous data (text logs and wearables).
* **Low latency** (< 200 ms p95) and scalability to thousands of concurrent users.
* **Separation of concerns** between user‑facing apps, API layer, machine learning and data pipelines.
* **Regulatory compliance** (HIPAA/GDPR) with auditability and encryption.

## Decision

1. **Client separation:** We build a React Native mobile app for patients and a Next.js web dashboard for clinicians. Each uses the API exclusively; no direct database access.
2. **API Service:** A FastAPI service running on GCP Cloud Run provides REST and WebSocket endpoints. It uses an async PostgreSQL client (`asyncpg`) to persist data and publishes events to Pub/Sub for downstream processing.
3. **ML Service:** A separate microservice hosts trained models. It exposes a simple HTTP endpoint and a TorchServe handler to perform inference and return explanations. The API calls this service via HTTP. Models are version‑pinned and loaded from a model registry.
4. **Data Pipeline:** Logs and wearable snapshots published to Pub/Sub are consumed by Apache Beam jobs running on Dataflow. These jobs store raw messages in GCS and build aggregate features in BigQuery. Feature tables are partitioned by event date.
5. **Infrastructure as Code:** All GCP resources (Cloud Run, Cloud SQL, Pub/Sub, BigQuery, IAM roles) are provisioned with Terraform in the `infra` module. This ensures reproducibility and version control.
6. **Observability:** OpenTelemetry instrumentation is integrated throughout the stack; metrics are exported to Prometheus and visualised in Grafana. Application logs are emitted in JSON format for structured analysis.

## Consequences

* **Flexibility:** Different teams can iterate on clients, API and ML independently.
* **Complexity:** Running multiple services introduces operational overhead (deployment pipelines, networking), but Cloud Run mitigates this by handling scaling and traffic shaping.
* **Scalability:** Each component scales horizontally based on demand; decoupled pipelines prevent back‑pressure on user‑facing services.
* **Security:** The split architecture restricts access patterns; the API service validates tokens and enforces RBAC. The ML service has no direct database access.
