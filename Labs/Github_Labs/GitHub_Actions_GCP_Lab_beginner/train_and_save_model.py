import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from google.cloud import storage
import joblib
from datetime import datetime

# Download necessary data - Iris data from sklearn library
# We define a function to download the data
def download_data():
  from sklearn.datasets import load_iris
  iris = load_iris()
  features = pd.DataFrame(iris.data, columns=iris.feature_names)
  target = pd.Series(iris.target)
  return features, target

# Define a function to preprocess the data
# In this case, preprocessing will be just splitting the data into training and testing sets
def preprocess_data(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  return X_train, X_test, y_train, y_test

# Define a function to train the model
def train_model(X_train, y_train):
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)
  return model

# Define a function to save the model both locally and in GCS
def save_model_to_gcs(model, bucket_name, blob_name):
  joblib.dump(model, "model.joblib")
  
  # Save the model to GCS
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(blob_name)
  blob.upload_from_filename('model.joblib')

# Putting all functions together
def main():
  # Download data
  X, y = download_data()
  X_train, X_test, y_train, y_test = preprocess_data(X, y)
  
  # Train model
  model = train_model(X_train, y_train)
  
  # Evaluate model
  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  print(f'Model accuracy: {accuracy}')
  
  # Save the model to gcs
  bucket_name = "github-actions-gcp-models-1"
  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  blob_name = f"trained_models/model_{timestamp}.joblib"
  save_model_to_gcs(model, bucket_name, blob_name)
  print(f"Model saved to gs://{bucket_name}/{blob_name}")
  
if __name__ == "__main__":
  main()

  
