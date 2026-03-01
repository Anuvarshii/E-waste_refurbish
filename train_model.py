import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv("dataset.csv")

# Inputs and Output
X = data[["physical_score","damage_score"]]
y = data["refurbish_value"]

# Create model
model = RandomForestRegressor(n_estimators=150, random_state=42)

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained and saved as model.pkl")
