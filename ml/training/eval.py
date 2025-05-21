"""Evaluation script for trained models.

Loads the model and evaluation data, computes metrics and prints them.
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score, brier_score_loss
from xgboost import XGBClassifier


MODEL_PATH = Path("ml/training/models/xgboost_model.json")


def load_model() -> XGBClassifier:
    model = XGBClassifier()
    model.load_model(MODEL_PATH)
    return model


def evaluate(model: XGBClassifier, df: pd.DataFrame) -> dict:
    X = df.drop(columns=["label"])
    y = df["label"]
    probs = model.predict_proba(X)[:, 1]
    return {
        "auprc": average_precision_score(y, probs),
        "auroc": roc_auc_score(y, probs),
        "f1": f1_score(y, probs > 0.5),
        "brier": brier_score_loss(y, probs),
    }


if __name__ == "__main__":
    df = pd.read_csv("ml/training/tests/test_data.csv") if Path("ml/training/tests/test_data.csv").exists() else None
    if df is None:
        df = pd.DataFrame()  # placeholder; evaluation requires dataset
        print("No test data found.")
    model = load_model()
    metrics = evaluate(model, df)
    print(metrics)