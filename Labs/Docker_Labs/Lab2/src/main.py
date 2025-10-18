# main.py
from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__, static_folder="statics")

# URL of your Flask API for making predictions (kept for parity)
api_url = "http://0.0.0.0:4000/predict"

# Load models & scaler
logreg_model = joblib.load("my_model.pkl")  # Logistic Regression
try:
    knn_model = joblib.load("knn_model.pkl")  # KNN (optional)
except Exception:
    knn_model = None
scaler = joblib.load("scaler.pkl")

class_labels = ["Setosa", "Versicolor", "Virginica"]

"""Modern web apps use a technique named routing. This helps the user remember the URLs. 
For instance, instead of having /booking.php they see /booking/. Instead of /account.asp?id=1234/ 
they’d see /account/1234/."""


@app.route("/")
def home():
    return "Welcome to the Iris Classifier API!"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            data = request.form
            sepal_length = float(data["sepal_length"])
            sepal_width = float(data["sepal_width"])
            petal_length = float(data["petal_length"])
            petal_width = float(data["petal_width"])

            # Prepare input (same shape as before) and scale
            input_data = np.array(
                [sepal_length, sepal_width, petal_length, petal_width]
            )[np.newaxis, :]
            input_scaled = scaler.transform(input_data)

            # Predict with Logistic Regression (kept behavior similar)
            pred_idx = int(logreg_model.predict(input_scaled)[0])
            predicted_class = class_labels[pred_idx]

            # Return JSON (same pattern as before)
            return jsonify({"predicted_class": predicted_class})
        except Exception as e:
            return jsonify({"error": str(e)})
    elif request.method == "GET":
        return render_template("predict.html")
    else:
        return "Unsupported HTTP method"


# Minimal twin endpoint for KNN, matching the style above
@app.route("/predict_knn", methods=["GET", "POST"])
def predict_knn():
    if request.method == "GET":
        return render_template("predict.html")
    try:
        if knn_model is None:
            return jsonify({"error": "KNN model not available in this image."}), 503

        data = request.form
        sepal_length = float(data["sepal_length"])
        sepal_width = float(data["sepal_width"])
        petal_length = float(data["petal_length"])
        petal_width = float(data["petal_width"])

        input_data = np.array([sepal_length, sepal_width, petal_length, petal_width])[
            np.newaxis, :
        ]
        input_scaled = scaler.transform(input_data)

        pred_idx = int(knn_model.predict(input_scaled)[0])
        predicted_class = class_labels[pred_idx]

        return jsonify({"predicted_class": predicted_class})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)
