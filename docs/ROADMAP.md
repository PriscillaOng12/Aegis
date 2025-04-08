# Roadmap

This roadmap outlines planned work for the next two quarters. Timelines are estimates and may shift based on user feedback and technical discoveries.

## Q3 2025 – MVP Delivery

| Initiative | Description | Owner | Milestone |
| --- | --- | --- | --- |
| MVP Feature Complete | Deliver v1 features: logging, risk scoring, baseline model, nudges, analytics dashboard | PM & Eng | 2025‑09‑30 |
| Infrastructure Harden | Finalise Terraform modules, enable Cloud Armor firewall rules, finish backup policies | DevOps | 2025‑09‑15 |
| Synthetic Data Launch | Release seed scripts and sample dataset; host developer demo on GitHub | DS & PM | 2025‑09‑20 |
| A/B Framework | Implement configuration for nudge timing/content; initial experiment design | PM & DS | 2025‑09‑25 |

## Q4 2025 – Scale & Real Integrations

| Initiative | Description | Owner | Milestone |
| --- | --- | --- | --- |
| HealthKit & Google Fit Integration | Build production adapters, handle per‑device consent flows | Mobile Team | 2025‑11‑15 |
| TFT Model Deployment | Train and deploy Temporal Fusion Transformer, improve AUROC and lead time | DS Team | 2025‑12‑01 |
| Enhanced Analytics | Add cohort comparisons, retention charts and intervention effectiveness metrics to dashboard | Web Team | 2025‑12‑20 |
| SLO Enforcement | Implement error budgets, alerting on SLO burn in Grafana; tune autoscaling parameters | SRE | 2025‑11‑30 |

## Stretch Goals

* **On‑Device Inference:** Investigate Core ML/TFLite deployment, evaluate battery impact, design incremental updates.  
* **Per‑User Calibration:** Use Bayesian approaches to personalise thresholds based on user behaviour.  
* **External Partnerships:** Integrate with pharmacy data to detect medication adherence and side‑effects.  
* **Research Portal:** Provide anonymised dataset for academic research, with strong governance and access controls.

## How to Contribute

Check out [`CONTRIBUTING.md`](../CONTRIBUTING.md) and open issues tagged with `help wanted`.
