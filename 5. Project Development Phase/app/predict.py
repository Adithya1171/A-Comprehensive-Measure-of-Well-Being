import os
import joblib
import numpy as np

MODEL_PATH = os.path.join("model", "model.pkl")
SCALER_PATH = os.path.join("model", "scaler.pkl")

# Global variables for model and scaler
_model = None
_scaler = None

def load_prediction_assets():
    """Loads the model and scaler files into memory."""
    global _model, _scaler
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Trained model or scaler assets are missing. Run train_model.py first.")
    
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    if _scaler is None:
        _scaler = joblib.load(SCALER_PATH)

def classify_hdi_category(score):
    """
    Classifies the HDI score into a development category.
    - Score >= 0.800: Very High
    - Score >= 0.700 and < 0.800: High
    - Score >= 0.550 and < 0.700: Medium
    - Score < 0.550: Low
    """
    if score >= 0.800:
        return "Very High"
    elif score >= 0.700:
        return "High"
    elif score >= 0.550:
        return "Medium"
    else:
        return "Low"

def predict_hdi(life_expectancy, mean_years_schooling, expected_years_schooling, gni_per_capita):
    """
    Validates input variables, runs the prediction model, and categorizes the result.
    
    Returns:
        (predicted_score, hdi_category)
    """
    # 1. Server-side range checks and validation
    try:
        le = float(life_expectancy)
        mys = float(mean_years_schooling)
        eys = float(expected_years_schooling)
        gni = float(gni_per_capita)
    except (ValueError, TypeError):
        raise ValueError("All inputs must be valid numeric values.")

    if not (20.0 <= le <= 100.0):
        raise ValueError("Life Expectancy must be between 20 and 100 years.")
    if not (0.0 <= mys <= 20.0):
        raise ValueError("Mean Years of Schooling must be between 0 and 20 years.")
    if not (0.0 <= eys <= 25.0):
        raise ValueError("Expected Years of Schooling must be between 0 and 25 years.")
    if gni <= 0.0:
        raise ValueError("Gross National Income per Capita must be positive.")

    # 2. Ensure model and scaler are loaded
    load_prediction_assets()

    # 3. Align input in exact order of features:
    # 1. Life Expectancy, 2. Mean Years of Schooling, 3. Expected Years of Schooling, 4. GNI per Capita
    import pandas as pd
    input_features = pd.DataFrame(
        [[le, mys, eys, gni]], 
        columns=["Life Expectancy", "Mean Years of Schooling", "Expected Years of Schooling", "GNI per Capita"]
    )

    # 4. Scale inputs using saved StandardScaler
    input_scaled = _scaler.transform(input_features)

    # 5. Predict raw HDI score
    raw_pred = _model.predict(input_scaled)[0]

    # 6. Clip predicted score between 0.000 and 1.000 (standard boundaries for index scores)
    predicted_score = max(0.0, min(1.0, float(raw_pred)))

    # 7. Classify category
    hdi_category = classify_hdi_category(predicted_score)

    return round(predicted_score, 4), hdi_category
