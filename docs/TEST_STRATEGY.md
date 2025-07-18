# Test Strategy

Testing in Aegis Health spans unit, integration, end‑to‑end (E2E) and load tests. This document outlines our approach and tooling.

## Unit Tests

* **API:** Use `pytest` and `httpx` to test FastAPI routes. Mock external services (Auth0, Pub/Sub). Validate Pydantic schemas, error handling and happy paths.
* **ML:** Test individual feature builders for correctness, ensuring rolling statistics handle edge cases (NaNs, daylight savings). Validate that model I/O matches the schema defined in `inference_schema.json`.
* **React/Next.js:** Use React Testing Library and Jest to test components. Mock network calls with MSW (Mock Service Worker).

## Integration Tests

* **API + Database:** Spin up Postgres via Docker; run migrations; seed test data; run API tests end‑to‑end, including authentication with a stub Auth0 server.
* **Pipeline:** Use `pytest` to run Beam jobs locally with the DirectRunner; verify that BigQuery schemas are honoured and partitioning works as expected.
* **Model + API:** Test the full flow: log symptoms, ingest wearables, call risk endpoint and trigger a nudge. Use synthetic data to exercise edge cases.

## End‑to‑End Tests

End‑to‑end tests simulate real user scenarios across the mobile and web clients. We use [Playwright](https://playwright.dev/) to script flows such as:

* A patient logs a symptom, receives a high risk notification and sees a nudge in the app.
* A clinician signs in, views the dashboard, triggers a manual intervention and observes analytics update.

E2E tests run nightly and on release candidates. Screenshots and traces are uploaded to artifacts for debugging.

## Load Tests

We use [k6](https://k6.io/) to simulate concurrent traffic. The script (`scripts/load_test.k6.js`) models user behaviour: logging symptoms, syncing wearables and polling risk scores. Load tests validate that p95 latency stays under 200 ms and error rate < 1 % for expected QPS. Results are stored in GitHub Actions artifacts and used to adjust resource allocations.

## Continuous Integration Gates

The CI pipeline (see `.github/workflows/ci.yml`) runs on every commit to `main` and pull request. Steps include:

1. **Static analysis:** `ruff`, `black`, `mypy`, ESLint and TSC ensure code quality.  
2. **Unit tests:** Run for API and ML services; fail build on any error.  
3. **Integration tests:** Execute pipeline and API integration tests.  
4. **Terraform validation:** Ensure infrastructure code is formatted and valid.  
5. **Docker builds:** Build API and ML images to catch Dockerfile errors early.

Only when all checks pass does the code merge. Smoke tests run after deployment (canary) to verify runtime health.

## Data Contracts

Data between components (API ↔ ML ↔ Pipeline) is governed by explicit schemas:

* `api/app/schemas` define request/response bodies. Tests ensure backwards compatibility by diffing against stored OpenAPI definitions.
* `ml/training/inference_schema.json` defines input/output fields for the model. Tests confirm that training features align with inference expectations.
* BigQuery schemas are versioned under `etl/infra/schemas`. Beam jobs validate that output tables conform to these schemas.

Breaking a contract requires bumping a version and migrating consumers. Tools such as [`schemathesis`](https://github.com/schemathesis/schemathesis) can fuzz test API contracts, although not yet integrated.
