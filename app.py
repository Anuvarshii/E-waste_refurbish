from flask import Flask, request, render_template
from config import TEMP_IMAGE_PATH
from services.image_processing import get_damage_score
from services.scoring import calculate_physical_score
from services.prediction import predict_refurbish_value
import datetime

app = Flask(__name__)


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/predictor")
def predictor():
    return render_template("predictor.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        uploaded_file = request.files["image"]
        uploaded_file.save(TEMP_IMAGE_PATH)

        brand = request.form["brand"]
        model = request.form["model"]
        year = int(request.form["year"])

        # Calculate age automatically
        current_year = datetime.datetime.now().year
        age = current_year - year

        # Battery mapping
        battery_status = request.form["battery_status"]

        battery_map = {
            "excellent": 90,
            "good": 75,
            "average": 55,
            "poor": 35
        }

        battery = battery_map.get(battery_status, 50)

        # Working condition calculation
        screen = request.form["screen"]
        touch = request.form["touch"]
        speaker = request.form["speaker"]
        camera = request.form["camera"]

        working = 0

        if screen == "yes":
            working += 2.5
        if touch == "yes":
            working += 2.5
        if speaker == "yes":
            working += 2.5
        if camera == "yes":
            working += 2.5

        # Physical score
        physical_score = calculate_physical_score(
            age,
            battery,
            working,
            brand
        )

        # CNN damage score
        damage_score = get_damage_score(TEMP_IMAGE_PATH)

        # Random Forest prediction
        refurbish_value, confidence = predict_refurbish_value(
            physical_score,
            damage_score
        )

        if refurbish_value >= 6:
            recommendation = "REFURBISH"
        else:
            recommendation = "RECYCLE"

        # Risk logic
        if refurbish_value >= 7:
            risk = "Low"
        elif refurbish_value >= 5:
            risk = "Medium"
        else:
            risk = "High"

        return render_template(
            "result.html",
            brand=brand,
            model=model,
            year=year,
            physical_score=round(physical_score, 2),
            damage_score=round(damage_score, 2),
            refurbish_value=round(refurbish_value, 2),
            confidence=confidence,
            recommendation=recommendation,
            risk=risk
        )

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)