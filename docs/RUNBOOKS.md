# Runbooks

Runbooks describe procedures for on‑call engineers to diagnose and resolve common issues in the Aegis Health platform. Each runbook includes severity levels, steps to reproduce, mitigation actions and points of contact.

## Service Down (API/ML)

**Symptoms:** 5xx errors returned from `/v1` endpoints or health check failures in Cloud Run. Dashboard shows error rate spike and API latency > 200 ms.

**Severity:** S1 – Service unavailable.

**Immediate Actions:**

1. **Acknowledge alert** in PagerDuty and join the incident Slack channel.
2. **Check Cloud Run status**:
   * Navigate to GCP console → Cloud Run → Services (api / ml). Inspect revision status.
   * If revision failed to deploy, roll back to previous revision from the UI.
3. **Examine logs** in Cloud Logging and Grafana. Look for exception traces, memory leaks, or database connection errors.
4. **Restart services** via `gcloud run services update` if a restart resolves the issue.
5. **If database is down:**
   * Check Cloud SQL instance health. If CPU > 80 % or connections maxed out, scale up instance or identify slow queries.
   * Failover to replica if configured.
6. **Communicate** status updates every 15 minutes in the incident channel until resolved.

**Post‑mortem:** After resolution, document the root cause, timeline and corrective actions. Schedule a retrospective with relevant teams. Capture action items in the backlog.

## Model Drift Detected

**Symptoms:** Decrease in AUPRC on daily monitoring; PSI (Population Stability Index) > 0.2 for key features. Clinician feedback of increased false positives.

**Severity:** S2 – Degraded performance.

**Actions:**

1. **Verify monitoring dashboards**: review drift metrics in Grafana. Identify which features or segments have drifted.
2. **Inspect training data freshness**: ensure the Dataflow jobs are running and BigQuery tables contain recent data.
3. **Retrain model**: run `ml/training/train.py` with latest data. Validate metrics offline (AUPRC, ECE) using `eval.py`.
4. **Deploy new model**: package it into a MAR file and update TorchServe config. Use canary deployment via GitHub Actions to route 10 % of traffic to the new model and monitor metrics.
5. **Roll back** if performance worsens or unexplained anomalies occur.

## Security Incident (PHI Exposure)

**Symptoms:** Suspicious access patterns in audit logs, unauthorised data export requests, or external notification of data leak.

**Severity:** S0 – Highest priority.

**Immediate Actions:**

1. **Contain**: Restrict database and storage access. Rotate credentials and revoke compromised tokens.
2. **Notify**: Escalate to security team, compliance officer and executives. Evaluate legal obligations for breach notification.
3. **Investigate**: Review audit logs to determine scope and timeline. Identify affected users and data types.
4. **Eradicate**: Remove malicious code or actors. Patch vulnerabilities and ensure they are not reopened.
5. **Recover**: Restore systems from backup if necessary. Monitor for further suspicious activity.
6. **Communicate**: Notify affected users as required by law. Provide remediation advice.

## Model Hotfix

Occasionally, a bug or data issue may necessitate a hotfix to the model outside of the standard release cycle.

1. **Reproduce the issue**: Write a failing test in `ml/training/tests` to capture the erroneous behaviour.
2. **Patch the model**: Update `ml/training/train.py` or data pipeline code. Train a small model on a subset of data to confirm the fix.
3. **Review**: Conduct a peer code review focusing on correctness and potential side effects.
4. **Deploy**: Package the new model; push a patch release using GitHub Actions. Monitor live metrics.
5. **Follow up**: Document the incident, reasons for bypassing full release cycle and steps to prevent recurrence.
