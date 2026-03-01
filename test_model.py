import joblib
import pandas as pd

model = joblib.load("model.pkl")

# Create DataFrame with proper column names
sample = pd.DataFrame({
    "physical_score": [7.5],
    "damage_score": [2.0]
})

prediction = model.predict(sample)

print("Predicted Refurbish Value:", round(prediction[0],2))

if prediction[0] >= 6:
    print("Recommendation: REFURBISH")
else:
    print("Recommendation: RECYCLE")