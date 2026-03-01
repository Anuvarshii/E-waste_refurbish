from flask import Flask, request, render_template
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image
import os

app = Flask(__name__)

rf_model = joblib.load("model.pkl")
from generate_dataset import refurbish_value
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

# Rebuild architecture
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

cnn_model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),   # ✅ MUST BE 256
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')
])

cnn_model.load_weights("damage_model.weights.h5")

# ---------- SCORING FUNCTIONS ----------

def age_score(age):
    if age <= 1: return 10
    elif age <= 2: return 8
    elif age <= 3: return 6
    elif age <= 4: return 4
    elif age <= 5: return 2
    else: return 1

def battery_score(battery):
    if battery >= 90: return 10
    elif battery >= 75: return 8
    elif battery >= 60: return 6
    elif battery >= 45: return 4
    elif battery >= 30: return 2
    else: return 1

def brand_score(brand):
    premium = ["apple", "samsung", "oneplus"]
    mid = ["vivo", "oppo", "realme"]
    budget = ["redmi", "poco", "motorola"]

    brand = brand.lower()

    if brand in premium: return 10
    elif brand in mid: return 8
    elif brand in budget: return 6
    else: return 3

def calculate_physical_score(age, battery, working, brand):
    a = age_score(age)
    b = battery_score(battery)
    br = brand_score(brand)
    return round((0.35*working)+(0.25*b)+(0.20*a)+(0.20*br),2)

# ---------- DAMAGE SCORE FROM CNN ----------

def get_damage_score(img_path):
    img = Image.open(img_path).convert("RGB").resize((224,224))
    img_array = np.array(img)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = cnn_model.predict(img_array)[0][0]

    # Cracked ≈ 0 → High damage
    damage_score = round((1 - prediction) * 10, 2)

    return damage_score

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    uploaded_file = request.files["image"]
    file_path = "temp.jpg"
    uploaded_file.save(file_path)

    brand = request.form["brand"]
    age = float(request.form["age"])
    battery = float(request.form["battery"])
    working = float(request.form["working"])

    physical_score = calculate_physical_score(age, battery, working, brand)
    damage_score = get_damage_score(file_path)

    input_data = pd.DataFrame({
        "physical_score":[physical_score],
        "damage_score":[damage_score]
    })

    refurbish_value = rf_model.predict(input_data)[0]

# Override logic for strong damage
    if damage_score >= 7:
     recommendation = "RECYCLE"
    elif damage_score <= 3:
     recommendation = "REFURBISH"
    else:
     recommendation = "REFURBISH" if refurbish_value >= 6 else "RECYCLE"

    return f"""
    Physical Score: {physical_score}<br>
    Damage Score (AI Detected): {damage_score}<br>
    Refurbish Value: {round(refurbish_value,2)}<br>
    Recommendation: {recommendation}
    """

if __name__ == "__main__":
    app.run(debug=True)