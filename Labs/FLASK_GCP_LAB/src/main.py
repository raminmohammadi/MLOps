from flask import Flask, request, jsonify
from predict import predict_iris
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get data as JSON
    sepal_length = float(data['sepal_length'])
    sepal_width = float(data['sepal_width'])
    petal_length = float(data['petal_length'])
    petal_width = float(data['petal_width'])

    print(sepal_length, sepal_width, petal_length, petal_width)

    prediction = predict_iris(sepal_length, sepal_width, petal_length, petal_width)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
