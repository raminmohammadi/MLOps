import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get the value of the environment variable
BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
VERSION_FILE_NAME = os.getenv('VERSION_FILE_NAME')


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from google.cloud import storage
import joblib
from datetime import datetime

# ----------------- Download ----------------- #
# Download necessary data - Iris data from sklearn library
# We define a function to download the data
def download_data():
  from sklearn.datasets import load_iris
  iris = load_iris()
  features = pd.DataFrame(iris.data, columns=iris.feature_names)
  target = pd.Series(iris.target)
  return features, target


# ----------------- Preprocess ----------------- #
# Define a function to preprocess the data
# In this case, preprocessing will be just splitting the data into training and testing sets
def preprocess_data(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  return X_train, X_test, y_train, y_test


# ----------------- Train model ----------------- #
# Define a function to train the model
def train_model(X_train, y_train):
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)
  return model


# ----------------- Model versioning ----------------- #
# A function to get the model version from GCS
def get_model_version(bucket_name, version_file_name):
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(version_file_name)
  if blob.exists():
    version_as_string = blob.download_as_text()
    version = int(version_as_string)
  else:
    version = 0
    
  return version


# ----------------- Update Model version ----------------- #
# A function to update the model version on GCS
def update_model_version(bucket_name, version_file_name, version):
  if not isinstance(version, int):
    raise ValueError("Version must be an integer")
  try:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(version_file_name)
    blob.upload_from_string(str(version))
    return True
  except Exception as e:
    print(f"Error updating model version: {e}")
    return False



# ----------------- Ensure folder exists ----------------- #
# A function to make sure file exist on GCS bucket
def ensure_folder_exists(bucket, folder_name):
  blob = bucket.blob(f"{folder_name}/")
  if not blob.exists():
    blob.upload_from_string('')
    print(f"Created folder: {folder_name}")



# ----------------- Save model to GCS ----------------- #
# Define a function to save the model both locally and in GCS
def save_model_to_gcs(model, bucket_name, blob_name):
  joblib.dump(model, "model.joblib")
  
  # Save the model to GCS
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  
  # Make sure the folder exists in GCS
  ensure_folder_exists(bucket, "trained_models")
  
  blob = bucket.blob(blob_name)
  blob.upload_from_filename('model.joblib')



# ----------------- Main function ----------------- #
# Putting all functions together
def main():
  # Get model version
  current_version = get_model_version(BUCKET_NAME, VERSION_FILE_NAME)
  new_version = current_version + 1
  
  # Download and preprocess data
  X, y = download_data()
  X_train, X_test, y_train, y_test = preprocess_data(X, y)
  
  # Train model
  model = train_model(X_train, y_train)
  
  # Evaluate model
  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  print(f'Model accuracy: {accuracy}')
  
  # Save the model to gcs with new version
  timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
  blob_name = f"trained_models/model_v{new_version}_{timestamp}.joblib"
  save_model_to_gcs(model, BUCKET_NAME, blob_name)
  print(f"Model saved to gs://{BUCKET_NAME}/{blob_name}")
  
  # Update version number on GCS if save was successful
  if update_model_version(BUCKET_NAME, VERSION_FILE_NAME, new_version):
    print(f"Model version updated to {new_version}")
    print(f"MODEL_VERSION_OUTPUT: {new_version}")
  else:
    print("Failed to update model version")
  


# ----------------- If statement to run main ----------------- #
if __name__ == "__main__":
  main()
# ----------------- If statement to run main ----------------- #
  
