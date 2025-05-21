import pandas as pd
from ml.training.train import generate_synthetic_data, train_model


def test_generate_synthetic_data():
    df = generate_synthetic_data(10)
    assert set(["pain", "fatigue", "nausea", "sleep_efficiency_mean_7d", "hrv_rmssd_mean_3d", "hr_mean_1d", "steps_sum_1d", "label"]) <= set(df.columns)


def test_train_model():
    df = generate_synthetic_data(200)
    metrics = train_model(df)
    assert 0 <= metrics["auprc"] <= 1
    assert 0 <= metrics["auroc"] <= 1