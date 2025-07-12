# ADR 0002 – Model Serving Strategy

## Status

Accepted – 2025‑08‑10

## Context

Our predictive model consumes both tabular features (rolling stats from wearables) and text embeddings. We need a serving layer that:

* Handles inference requests in under 80 ms.
* Provides explanation for clinicians (top drivers via SHAP values).
* Allows A/B experimentation with different model architectures (XGBoost vs TFT).
* Supports versioned models and rollback.
* Is easily deployable on GCP Cloud Run.

## Decision

1. **TorchServe** is selected as the model server. It has first‑class support for PyTorch models and plug‑in handlers. Although our baseline model is XGBoost, we wrap it in a TorchScript module using the `ml/serving/handler.py` adapter. Future TFT models can be loaded natively. TorchServe also exposes a `/predictions` endpoint by default.
2. **Custom handler:** We implement a custom handler that loads the scaler and encoding artefacts, constructs features from the request payload, executes the model, calculates calibrated probabilities and generates SHAP values using the saved explainer.
3. **Health checks:** The handler implements the `handle` method plus an explicit `ping` route for readiness. TorchServe’s built‑in metrics can be scraped by Prometheus via `prometheus.txt`.
4. **Versioning:** Models are packaged into MAR files with version numbers (`model_v1.mar`); the CI/CD pipeline updates TorchServe config to pin the desired version. Rollback is as simple as switching the model version in the config.
5. **Decoupling:** The API service calls the ML service via HTTP; this separation allows independent scaling and avoids coupling deployment cycles.

## Consequences

* **Increased complexity:** Packaging non‑PyTorch models into MAR files introduces a build step. However, it unifies serving across models and simplifies on‑call operations.
* **Explainability:** SHAP calculations on large inputs add overhead. To meet latency budgets, we pre‑compute background datasets and limit the number of features shown in explanations.
* **Extensibility:** Future models (e.g., TFT or personalised models) can be added as additional handlers without changing the API layer.
