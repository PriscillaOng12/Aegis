"""TorchServe handler for Aegis Health model.

This handler wraps an XGBoost model saved as JSON and returns calibrated
probabilities and SHAP-based explanations. It expects input JSON matching
`inference_schema.json`.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, Any

from xgboost import XGBClassifier
import shap


MODEL_PATH = Path("/home/model-server/model_store/xgboost_model.json")
BACKGROUND_PATH = Path("/home/model-server/model_store/shap_background.json")


class ModelHandler:
    def __init__(self):
        self.model: XGBClassifier | None = None
        self.explainer: shap.TreeExplainer | None = None

    def initialize(self, ctx):
        # Load model
        self.model = XGBClassifier()
        self.model.load_model(MODEL_PATH)
        # Load SHAP background
        with open(BACKGROUND_PATH) as f:
            background = json.load(f)["background"]
        self.explainer = shap.TreeExplainer(self.model, data=np.array(list(zip(*background.values()))))

    def preprocess(self, data: Dict[str, Any]) -> np.ndarray:
        return np.array([
            [
                data["pain"],
                data["fatigue"],
                data["nausea"],
                data["sleep_efficiency_mean_7d"],
                data["hrv_rmssd_mean_3d"],
                data["hr_mean_1d"],
                data["steps_sum_1d"],
            ]
        ])

    def inference(self, input_array: np.ndarray) -> Dict[str, Any]:
        prob = float(self.model.predict_proba(input_array)[0][1])
        shap_values = self.explainer.shap_values(input_array)
        top_idx = np.argsort(np.abs(shap_values[0]))[::-1][:3]
        feature_names = ["pain", "fatigue", "nausea", "sleep_efficiency_mean_7d", "hrv_rmssd_mean_3d", "hr_mean_1d", "steps_sum_1d"]
        drivers = [
            {"feature": feature_names[i], "impact": float(shap_values[0][i])}
            for i in top_idx
        ]
        return {
            "risk_percentage": prob,
            "top_drivers": drivers,
            "lead_time_hours": None,
        }

    def handle(self, data, ctx):
        if not data:
            return []
        input_json = data[0].get("body")
        if isinstance(input_json, (bytes, bytearray)):
            input_json = input_json.decode()
        payload = json.loads(input_json)
        x = self.preprocess(payload)
        return [self.inference(x)]