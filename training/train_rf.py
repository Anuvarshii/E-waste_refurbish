import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv("dataset.csv")

# Features
X = data[["physical_score", "damage_score"]]

# Target
y = data["refurbish_value"]

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save model
joblib.dump(model, "../models/model.pkl")

print("Random Forest model retrained and saved successfully.")