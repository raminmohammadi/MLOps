import pandas as pd
import joblib
import io
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from google.cloud import storage

def download_data():
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target)
    return X, y

def preprocess_data(X, y):
    # random_state ensures reproducibility
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def save_model_to_gcs(model, bucket_name, blob_name):
    """Saves model directly to GCS using an in-memory buffer."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Use a buffer to avoid writing to local disk
        buffer = io.BytesIO()
        joblib.dump(model, buffer)
        buffer.seek(0)
        
        blob.upload_from_file(buffer, content_type='application/octet-stream')
        print(f"✅ Model successfully uploaded to gs://{bucket_name}/{blob_name}")
    except Exception as e:
        print(f"❌ Failed to upload model: {e}")

def main():
    # Use environment variables for flexibility
    bucket_name = os.getenv("GCS_BUCKET_NAME", "github-action-lab")
    
    # Execution steps
    X, y = download_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    
    model = train_model(X_train, y_train)
    
    # Evaluation
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f'Model accuracy: {accuracy:.4f}')
    
    # Versioning
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    blob_name = f"trained_models/iris_rf_{timestamp}.joblib"
    
    save_model_to_gcs(model, bucket_name, blob_name)

if __name__ == "__main__":
    main()