# ADR 0003 – Data Retention & Privacy

## Status

Accepted – 2025‑08‑10

## Context

Aegis Health captures potentially sensitive health information, including symptom narratives and physiological data. Regulations (HIPAA, GDPR) require that we minimise the data stored, obtain consent and allow users to delete or export their data. We must also support research on aggregated, anonymised data.

## Decision

1. **Pseudonymous IDs:** We store user records with a generated UUID and keep the Auth0 subject identifier in a separate table (`auth_identities`). This decouples identity from health records.
2. **Per‑tenant isolation:** Each clinician group (tenant) is mapped to its own schema in Postgres; queries are scoped by tenant ID. This reduces risk of cross‑tenant data leakage.
3. **Consent flags:** Tables such as `wearable_snapshots` and `symptom_logs` include a `consent` boolean. Users can toggle streams and revoke consent at any time via the mobile app. When consent is withdrawn, no further data is stored.
4. **Retention period:** Raw logs (free text and wearable snapshots) are retained in GCS for 90 days by default, after which they are deleted. Aggregated features in BigQuery are retained for 2 years for research with anonymisation. Retention policies are configurable via Terraform.
5. **Deletion & export:** We implement endpoints to allow users to request deletion or export of their data. Deletion cascades through related tables. Exports are delivered as encrypted ZIP files via GCS signed URLs.

## Consequences

* **Compliance:** We meet GDPR Articles 17 and 20 and HIPAA regulations by providing explicit consent mechanisms and honouring deletion requests.
* **Operational overhead:** Retention policies require scheduled jobs to purge data and verify that deletion is complete. We implement Cloud Scheduler cron jobs for this purpose.
* **Research trade‑off:** Longer retention of aggregated features balances privacy with the need for longitudinal analysis. We anonymise features (remove identifiers) before storing them.
