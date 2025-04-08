# Product Requirements Document (PRD) – Aegis Health

## Purpose

Aegis Health empowers individuals living with chronic conditions to better manage their health by predicting 48‑hour flare‑ups from self‑reported symptoms and wearable signals. Timely nudges improve adherence to treatment plans and reduce unnecessary clinic visits. Clinicians gain a dashboard to monitor patient adherence, evaluate nudge effectiveness and adjust interventions.

## Goals & Success Metrics

**Primary goal:** Reduce the frequency and severity of flare‑ups by delivering proactive interventions.

**Success metrics:**

| Metric | Definition | Target |
| --- | --- | --- |
| AUPRC | Area under the precision–recall curve on held‑out users | ≥ 0.45 |
| Calibration error (ECE) | Expected calibration error on inference | ≤ 3 % |
| Crash‑free sessions | Percentage of sessions without unhandled crashes | > 99.5 % |
| Adherence uplift | Relative increase in symptom logging after nudges | +15 % over baseline |
| Lead‑time median | Median hours from risk prediction to recorded flare‑up | ≥ 12 h |
| DAU/WAU | Daily active users vs weekly active users | > 30 % |

## Personas

### Patient

*Lives with a chronic autoimmune disorder.* Regularly experiences flare‑ups but struggles to identify triggers. Seeks a simple logging tool and early warnings. Values privacy, ease of use and actionable insights.

### Clinician

*Rheumatologist or nurse practitioner.* Oversees a cohort of patients. Needs aggregated metrics on adherence, false‑alert rates and lead times. Wishes to adjust nudge messages and view risk histories. Requires HIPAA compliance and auditability.

### Data Scientist

*Develops models to predict flare‑ups.* Needs robust pipelines, reproducible datasets and ability to iterate on architectures. Monitors model drift and calibration. Balances performance with interpretability for clinical acceptance.

## User Stories (v1)

1. **As a patient, I can log my symptoms** (free text and severity sliders) so that I can track my condition over time.
2. **As a patient, I receive just‑in‑time nudges** when my risk is high so that I can take preventive action.
3. **As a clinician, I view a dashboard** summarising adherence, false‑alert rate and lead‑time metrics for my patients.
4. **As a clinician, I can customise nudge templates** to better suit my patient population.
5. **As a patient, I can export and delete my data** to comply with privacy laws (GDPR/CCPA).
6. **As a data scientist, I can retrain models on fresh data** via pipelines that protect against data leakage and ensure reproducibility.

## Constraints & Assumptions

* Wearable adapters will initially support Apple HealthKit and Google Fit; future extensions (e.g., Garmin, Oura) must not require backend changes.
* Prediction horizon is fixed at 48 hours in v1; later versions may support configurable horizons.
* Offline‑first mobile experience; network loss must not block symptom logging.
* Users’ timezone is stored and used when generating feature windows.

## V1 Scope

* Mobile and web clients with core logging and analytics flows.
* Baseline XGBoost model trained on synthetic data.
* Nudges delivered via push notifications and in‑app banners.
* Terraform‑provisioned GCP infrastructure (Cloud Run, Cloud SQL, Pub/Sub, BigQuery).
* Synthetic seed data generator for demonstration.

## Out of Scope (v1)

* On‑device inference (Core ML/TFLite) – planned for v2.
* Per‑user calibration layers – planned for v2.
* Real wearable integrations (beyond mock adapters) – integration to be scheduled once data contracts are finalised.
* Internationalisation/localisation – English only in v1.

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **Model drift** as more users onboard | Predictive performance degrades | Monitor drift via PSI and schedule periodic retraining |
| **Data privacy incidents** | Breach of sensitive health information | Follow least‑privilege principle, encrypt data at rest/in transit, audit accesses |
| **Low adherence** to symptom logging | Insufficient data for predictions | Use gamification and helpful nudges to encourage logging |
| **False positives** causing alert fatigue | Users may ignore notifications | Calibrate thresholds, evaluate false‑alert rate and tune model accordingly |

## Version 2 Preview

* Support on‑device inference for instant risk updates without network latency.
* Real‑time wearables ingestion via HealthKit and Google Fit APIs.
* Personalised models per user; meta‑learning for new users.
* Additional analytics: correlation between interventions and outcomes.
