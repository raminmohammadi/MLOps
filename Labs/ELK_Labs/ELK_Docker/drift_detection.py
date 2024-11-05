import logging
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from random import randint, random

# Configure logging
logging.basicConfig(filename='logstash/drift_detection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Data generation function to simulate drift
def generate_data(samples=1000, features=20, drift=False):
    X, y = make_classification(n_samples=samples, n_features=features, n_informative=15, random_state=randint(0, 1000))
    if drift:
        # Introduce drift by scaling some features differently
        X[:, 0] *= np.random.uniform(1.5, 2.0)
        X[:, 1] += np.random.normal(0, 5, size=samples)
    return X, y

# Preprocessing pipeline with logging
def preprocess_data(X, scaler=None):
    logging.info("Starting data preprocessing.")
    if scaler is None:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        logging.info("Fitting and transforming data using StandardScaler.")
    else:
        X_scaled = scaler.transform(X)
        logging.info("Transforming data using existing StandardScaler.")
    return X_scaled, scaler

# Model training pipeline with randomness and logging
def train_model(X_train, y_train):
    # Randomize hyperparameters to introduce variability in performance
    model = LogisticRegression(
        C=np.random.uniform(0.1, 1.0),  # Regularization strength
        max_iter=np.random.randint(50, 200),  # Random number of iterations
        solver=np.random.choice(['liblinear', 'saga'])
    )
    logging.info("Starting model training with randomized hyperparameters.")
    model.fit(X_train, y_train)
    logging.info("Model training completed.")
    return model

# Function to simulate data drift detection and log each instance
def detect_drift(X_batch, scaler, batch_count):
    # Introduce drift in 5% of the batch
    drift_indices = np.random.choice(len(X_batch), int(0.05 * len(X_batch)), replace=False)
    drift_detected = False

    for idx in drift_indices:
        # Modify feature values to create schema or statistical mismatches
        if random() > 0.5:
            X_batch[idx][0] *= np.random.uniform(1.5, 2.0)  # Statistically different
            drift_type = "statistical change"
        else:
            X_batch[idx] = np.append(X_batch[idx][1:], np.random.uniform(-10, 10))  # Schema mismatch
            drift_type = "schema change"
        
        # Log each drift instance with structured message
        logging.warning(f"Data drift detected in batch {batch_count} - sample_index: {idx}, drift_type: {drift_type}")
        drift_detected = True

    if drift_detected:
        logging.info(f"Data drift detected in batch {batch_count}. Drift reported in {len(drift_indices)} out of {len(X_batch)} samples.")

# Main loop to simulate pipeline execution for 10 minutes
def main():
    # Generate initial training and test data
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocess training data
    X_train_processed, scaler = preprocess_data(X_train)
    model = train_model(X_train_processed, y_train)

    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=10)
    batch_count = 0

    # Loop to simulate feeding batches of test data every minute
    while datetime.now() < end_time:
        # Generate a batch of test data and preprocess it
        X_batch, y_batch = generate_data(samples=64)
        X_batch_processed, _ = preprocess_data(X_batch, scaler=scaler)

        # Detect data drift in the batch
        detect_drift(X_batch_processed, scaler, batch_count)

        # Log model prediction performance
        predictions = model.predict(X_batch_processed)
        f1 = f1_score(y_batch, predictions, average='weighted')
        logging.info(f"Batch {batch_count}: Model F1 score on current batch: {f1:.2f}")

        # Wait for a minute before processing the next batch
        batch_count += 1
        time.sleep(60)

    logging.info("Pipeline execution finished after 10 minutes.")

if __name__ == "__main__":
    main()
