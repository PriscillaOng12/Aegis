# Aegis Health: AI Symptom & Side‑Effect Tracker

Welcome to **Aegis Health**, an end‑to‑end platform for predicting health flare‑ups within the next 48 hours.  
The system ingests free‑text symptom logs and wearable signals (heart rate, HRV, sleep, steps), predicts the risk of a flare‑up, and surfaces timely nudges to users and caregivers.  

This repository contains everything required to run the mobile app, web dashboard, backend API, machine learning service, ETL pipelines and infrastructure. It is structured as a monorepo with clear separation between components and comprehensive documentation.

## Why Aegis Health?

* **Patient empowerment** – Logging symptoms is frictionless with support for free text and sliders.  
* **Proactive care** – Predictive models anticipate adverse events so interventions arrive before users suffer.  
* **Clinician insight** – The dashboard highlights adherence, false‑alert rates and retention metrics.  
* **Robust & secure** – Built with audited libraries, encryption at rest and in transit, and strong RBAC.

## Architecture Overview

The system consists of four major subsystems:

1. **Mobile Client (React Native / Expo):** Patients log symptoms, view risk cards and receive push notifications.  
2. **Web Client (Next.js):** Clinicians monitor their cohort, review analytics and adjust nudge templates.  
3. **Backend API (FastAPI):** Serves REST and WebSocket endpoints, handles authentication via Auth0, persists data in Postgres and publishes events to Pub/Sub.  
4. **Machine Learning Service (PyTorch Lightning + TorchServe):** Trains models on logs and wearable data, generates calibrated risk scores and explains top drivers via SHAP.  
5. **Data Pipeline (Apache Beam on Dataflow):** Ingests logs and wearable snapshots into BigQuery feature tables for training and real‑time inference.

An ASCII diagram summarises the high‑level architecture:

```
  Mobile App        Web Dashboard
      |                   |
      | REST + WebSocket  |
      v                   v
   FastAPI API  <---- Auth0 ---->  Clinicians
      |\              |\
      | \   Pub/Sub   | \               Grafana
      |  \  messages  |  \-- Telemetry --> Prometheus
      v   \           v
    Postgres \     Dataflow (Beam)
              \         |
               \        v
                \--> BigQuery
                ML Service (TorchServe)
```

## Quickstart

This repo is designed to run end‑to‑end with minimal setup. Use the [`Makefile`](./Makefile) to orchestrate tasks.

### Requirements

* **Python 3.11+** and **Node.js 18+**  
* **Docker** and **Docker Compose**  
* **Terraform** (≥ 1.3) for infrastructure provisioning  
* An Auth0 tenant (for local development you can use a dev tenant configured in `.env`)

### Local Development

```bash
# clone the repository
git clone https://example.com/aegis-health.git
cd aegis-health

# install project dependencies and pre‑commit hooks
make setup

# generate synthetic data and train the baseline model
make seed

# run API and ML services locally with docker compose
make dev

# run the mobile app (requires Expo CLI installed globally)
cd frontend-mobile && npm install && npx expo start

# run the web dashboard
cd ../frontend-web && npm install && npm run dev

# run tests and static analysis
make test
make lint
make typecheck
```

### Deploying to GCP

Deployment is automated via Terraform and GitHub Actions.  
You will need to provide GCP credentials and Auth0 settings in the `infra/variables.tf` or through a Terraform `.tfvars` file.  
To provision infrastructure and deploy the services:

```bash
cd infra
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

Once infrastructure is live, GitHub Actions will build and push container images to Google Container Registry and update Cloud Run revisions. See `.github/workflows/ci.yml` for details.

### Frequently Asked Questions (FAQ)

**Q:** Do I need actual wearables to test the pipeline?  
**A:** No. The seed script (`scripts/seed_data.py`) generates synthetic wearable snapshots and symptom logs. You can plug in Apple Health or Google Fit adapters later.

**Q:** How do I regenerate the OpenAPI specification?  
**A:** Run `make openapi` in the `api` directory. This uses FastAPI’s built‑in OpenAPI generator.

**Q:** Where are secrets stored?  
**A:** Secrets are never checked into the repository. For local runs they come from a `.env` file; in GCP they live in Secret Manager and are injected via Cloud Run environment variables.

For more information see [`docs/PRODUCT_PRD.md`](./docs/PRODUCT_PRD.md) and our ADR series under `docs/ADR/`.
