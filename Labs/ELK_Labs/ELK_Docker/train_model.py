import logging
import time
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix
from datetime import datetime, timedelta

# Configure the logging module
logging.basicConfig(filename='logstash/training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Iris dataset once
data = load_iris()
X, y = data.data, data.target

# Track start time
start_time = datetime.now()
end_time = start_time + timedelta(minutes=20)

# Loop to retrain the model every 2 minutes with added randomness, stopping after 20 minutes
while datetime.now() < end_time:
    # Split the data into training and testing sets with a different random state each time
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=np.random.randint(1000))

    # Add random noise to the training data to increase randomness
    feature_noise = np.random.normal(0, 0.1, X_train.shape)
    X_train_noisy = X_train + feature_noise

    # Randomly flip some labels in y_train to add more variation
    label_noise = np.random.binomial(1, 0.1, size=y_train.shape)  # 10% label noise
    y_train_noisy = np.where(label_noise == 1, np.random.choice(np.unique(y)), y_train)

    # Initialize the Logistic Regression model with random hyperparameters
    model = LogisticRegression(
        penalty=np.random.choice(['l1', 'l2', 'elasticnet', 'none']),
        solver=np.random.choice(['liblinear', 'saga']),
        C=np.random.uniform(0.1, 1.0),  # Regularization strength
        max_iter=np.random.randint(50, 200)  # Random number of iterations
    )

    # Logging important information
    logging.info("Starting model training...")
    logging.info(f"Number of training samples: {len(X_train)}")
    logging.info(f"Number of testing samples: {len(X_test)}")

    # Train the model with noisy data and log progress
    try:
        model.fit(X_train_noisy, y_train_noisy)
        logging.info("Model training completed.")
    except Exception as e:
        logging.error(f"Model training failed: {e}")
        continue

    # Evaluate the model
    predictions = model.predict(X_test)
    score = model.score(X_test, y_test)
    logging.info(f"Model accuracy on test data: {score:.2f}")

    # Additional metrics
    f1 = f1_score(y_test, predictions, average='weighted')
    conf_matrix = confusion_matrix(y_test, predictions)

    tp = np.diag(conf_matrix)
    tn = np.sum(conf_matrix) - (np.sum(conf_matrix, axis=0) + np.sum(conf_matrix, axis=1) - tp)
    fp = np.sum(conf_matrix, axis=0) - tp
    fn = np.sum(conf_matrix, axis=1) - tp

    # Calculate rates
    fp_rate = np.divide(fp, (fp + tn), out=np.zeros_like(fp, dtype=float), where=(fp + tn) != 0)
    fn_rate = np.divide(fn, (fn + tp), out=np.zeros_like(fn, dtype=float), where=(fn + tp) != 0)

    # Log additional metrics
    logging.info(f"F1 Score: {f1:.2f}")
    logging.info(f"True Negative: {tn}")
    logging.info(f"False Positive: {fp}")
    logging.info(f"False Negative: {fn}")
    logging.info(f"True Positive: {tp}")
    logging.info(f"False Positive Rate: {fp_rate}")
    logging.info(f"False Negative Rate: {fn_rate}")

    # Log model parameters
    logging.info(f"Model coefficients: {model.coef_}")
    logging.info(f"Model intercept: {model.intercept_}")

    # Wait 2 minutes before retraining
    logging.info("Waiting 2 minutes before next training run...\n")
    time.sleep(120)

logging.info("Training loop finished after 20 minutes.")
