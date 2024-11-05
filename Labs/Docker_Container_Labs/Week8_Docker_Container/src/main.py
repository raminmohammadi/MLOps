from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# URL of your Flask API for making predictions
api_url = 'http://0.0.0.0:4000/predict'  # Update with the actual URL

# Load the TensorFlow model
model = tf.keras.models.load_model('my_model.keras')  # Replace 'my_model.keras' with the actual model file
class_labels = ['Setosa', 'Versicolor', 'Virginica']


"""Modern web apps use a technique named routing. This helps the user remember the URLs. 
For instance, instead of having /booking.php they see /booking/. Instead of /account.asp?id=1234/ 
they’d see /account/1234/."""

@app.route('/')
def home():
    return "Welcome to the Iris Classifier API!"

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.form
            sepal_length = float(data['sepal_length'])
            sepal_width = float(data['sepal_width'])
            petal_length = float(data['petal_length'])
            petal_width = float(data['petal_width'])

            # Perform the prediction
            input_data = np.array([sepal_length, sepal_width, petal_length, petal_width])[np.newaxis, ]
            prediction = model.predict(input_data)
            predicted_class = class_labels[np.argmax(prediction)]

            # Return the predicted class in the response
            # Use jsonify() instead of json.dumps() in Flask
            return jsonify({"predicted_class": predicted_class})
        except Exception as e:
            return jsonify({"error": str(e)})
    elif request.method == 'GET':
        return render_template('predict.html')
    else:
        return "Unsupported HTTP method"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
