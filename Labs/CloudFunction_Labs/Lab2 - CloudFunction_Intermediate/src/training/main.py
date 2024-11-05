import base64
import json
from google.cloud import storage
import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def train_model(event, context):
    """Triggered by Pub/Sub to start model training."""
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    file_name = message.get('file')

    # Initialize Cloud Storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket('BUCKET_NAME')
    blob = bucket.blob(file_name)
    file_contents = blob.download_as_text()

    from io import StringIO
    data = pd.read_csv(StringIO(file_contents))

    # Separate features and target
    X = data.drop('species', axis=1)  # Drop 'species' which is the target label
    y = data['species']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    model_path = '/tmp/model.pkl'
    with open(model_path, 'wb') as model_file:
        joblib.dump(clf, model_file)

    # Upload the model to Cloud Storage
    model_blob = bucket.blob('model.pkl')
    model_blob.upload_from_filename(model_path)

    print('Model trained and saved to Cloud Storage')
    return 'Model trained and saved to Cloud Storage'
