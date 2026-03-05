import joblib
import pandas as pd
import numpy as np
from config import MODEL_PATH

rf_model = joblib.load(MODEL_PATH)

def predict_refurbish_value(physical_score, damage_score):

    input_data = pd.DataFrame({
        "physical_score":[physical_score],
        "damage_score":[damage_score]
    })

    # Final prediction
    value = rf_model.predict(input_data)[0]

    # Predictions from each tree
    tree_preds = [tree.predict(input_data)[0] for tree in rf_model.estimators_]

    # Measure agreement between trees
    std_dev = np.std(tree_preds)

    # Convert to confidence (lower std = higher confidence)
    confidence = max(40, min(95, 100 - std_dev * 20))

    return round(value,2), round(confidence,2)