# Product Strategy – Aegis Health

## Vision

Enable every individual living with a chronic condition to anticipate and prevent flare‑ups before they happen. We believe that combining behavioural data (symptoms, adherence) and physiological signals yields a holistic understanding of health trajectories. Aegis Health serves as the intelligent companion bridging patients, clinicians and data scientists.

## Competitive Landscape

| Competitor | Focus | Differentiators |
| --- | --- | --- |
| *Whoop/Elite health trackers* | Consumer wearables focused on athletes; emphasise HRV and recovery but not clinical outcomes | Our system couples unstructured symptom narratives with wearables, providing context for chronic disease populations |
| *Health apps with journaling* | Allow users to record symptoms and triggers manually | Aegis introduces predictive modelling and actionable nudges, not just retrospective journaling |
| *Clinical portals (Epic/Telehealth)* | Centralised EHR interfaces for providers | We integrate patient‑generated data directly and provide real‑time risk scoring, reducing manual triage workload |

## Positioning & Target Audience

Aegis Health positions itself as a privacy‑conscious AI companion for chronic disease management. The primary target is chronic illness patients (e.g., autoimmune, fibromyalgia) aged 25–55 who own a smartphone and optionally a wearable. Secondary audiences include clinicians interested in remote monitoring and research teams analysing flare‑up predictors.

## North‑Star Metric

**Proportion of flare‑ups predicted at least 12 hours in advance with less than 20 % false positives.**  
This metric encapsulates both predictive power (precision/recall) and practical lead time for patients to act.

## Roadmap & Bets

### Q3 2025 – MVP Delivery (This Repository)

* Launch mobile logging, baseline model and nudges to a limited cohort.  
* Provision GCP infrastructure with Terraform and instrument services with observability.  
* Validate core risk scoring pipeline with synthetic data and gather clinician feedback.

### Q4 2025 – Scale & Real Integrations

* Integrate Apple HealthKit and Google Fit adapters; ingest real wearable data.  
* Deploy TFT model for improved temporal dynamics; implement calibration layer.  
* Expand analytics dashboard with cohort comparisons and trending charts.

### Q1 2026 – Personalisation & On‑Device Inference

* Introduce meta‑learning to warm‑start models for new users.  
* Deliver TFLite/Core ML inference to reduce latency and allow offline risk updates.  
* Conduct A/B tests on nudge timing and content, optimising for adherence uplift.

### Risks & Mitigations

* **Privacy regulation changes:** We track evolving HIPAA/GDPR requirements. Mitigation: have compliance guardrails (see `docs/COMPLIANCE_GUARDRAILS.md`), maintain pseudonymous IDs and consent flags.
* **Model acceptance by clinicians:** Without trust, adoption is limited. Mitigation: provide interpretable drivers via SHAP, calibrate probabilities and maintain transparent model cards.
* **Platform fragmentation:** Supporting multiple wearables and OS versions can slow velocity. Mitigation: define clear data contracts and use abstraction layers for integrations.
