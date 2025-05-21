"""Training script for the Aegis Health baseline model.

This script generates a synthetic dataset with text and wearable features,
trains an XGBoost classifier and evaluates performance. It saves the model
and artefacts to the `models/` directory along with a SHAP explainer.
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score
from xgboost import XGBClassifier
import shap


OUT_DIR = Path("ml/training/models")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_synthetic_data(n: int = 1000) -> pd.DataFrame:
    """Generate a synthetic dataset for demonstration purposes."""
    rng = np.random.default_rng(seed=42)
    data = pd.DataFrame({
        "pain": rng.integers(0, 11, size=n),
        "fatigue": rng.integers(0, 11, size=n),
        "nausea": rng.integers(0, 11, size=n),
        "sleep_efficiency_mean_7d": rng.uniform(0.5, 1.0, size=n),
        "hrv_rmssd_mean_3d": rng.uniform(20, 80, size=n),
        "hr_mean_1d": rng.uniform(50, 90, size=n),
        "steps_sum_1d": rng.uniform(0, 10000, size=n),
    })
    # Label: flare if pain or fatigue exceeds threshold or random spike
    data["label"] = ((data["pain"] >= 7) | (data["fatigue"] >= 7) | (rng.random(n) < 0.1)).astype(int)
    return data


def train_model(df: pd.DataFrame) -> dict:
    X = df.drop(columns=["label"])
    y = df["label"]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        max_depth=4,
        learning_rate=0.1,
        n_estimators=100,
        subsample=0.8,
        colsample_bytree=0.8,
    )
    model.fit(X_train, y_train)
    # Evaluate
    y_prob = model.predict_proba(X_val)[:, 1]
    metrics = {
        "auprc": average_precision_score(y_val, y_prob),
        "auroc": roc_auc_score(y_val, y_prob),
        "f1": f1_score(y_val, y_prob > 0.5),
    }
    # Save model
    model.save_model(str(OUT_DIR / "xgboost_model.json"))
    # Compute SHAP values on a sample
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_train.iloc[:100])
    with open(OUT_DIR / "shap_background.json", "w") as f:
        json.dump({"background": X_train.iloc[:100].to_dict(orient="list")}, f)
    return metrics


if __name__ == "__main__":
    df = generate_synthetic_data(2000)
    metrics = train_model(df)
    print("Training complete. Metrics:", metrics)