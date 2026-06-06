import numpy as np
import joblib

# Load trained landslide model
model = joblib.load("app/models/landslide_model.pkl")


def predict_landslide(features: list):
    """
    Predict landslide risk using ML model
    """

    # convert input into model format
    data = np.array(features).reshape(1, -1)

    prediction = model.predict(data)[0]

    # convert model output → risk level
    if prediction == 2:
        return "HIGH"
    elif prediction == 1:
        return "MEDIUM"
    else:
        return "LOW"