import joblib
from google.cloud import storage
import numpy as np
import json

model = None
def load_model():
    """Downloads and loads the model from Cloud Storage."""
    global model
    if model is None:
        storage_client = storage.Client()
        bucket = storage_client.bucket('BUCKET_NAME')
        blob = bucket.blob('model.pkl')
        blob.download_to_filename('/tmp/model.pkl')
        model = joblib.load('/tmp/model.pkl')
        print('Model loaded from Cloud Storage')


def predict(request):
    """HTTP Cloud Function to handle prediction requests."""
    global model
    load_model()

    request_json = request.get_json()
    if not request_json or 'features' not in request_json:
        return json.dumps({'error': 'Invalid input'}), 400

    features = np.array(request_json['features']).reshape(1, -1)
    prediction = model.predict(features)

    return json.dumps({'prediction': prediction.tolist()})

