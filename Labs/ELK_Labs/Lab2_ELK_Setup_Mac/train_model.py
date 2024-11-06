import logging
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix
import numpy as np

# Configure the logging module
logging.basicConfig(filename='training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Iris dataset
data = load_iris()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Logistic Regression model
model = LogisticRegression()

# Logging important information
logging.info("Starting model training...")
logging.info(f"Number of training samples: {len(X_train)}")
logging.info(f"Number of testing samples: {len(X_test)}")

# Training the model and logging progress
model.fit(X_train, y_train)
logging.info("Model training completed.")

# Evaluate the model
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
logging.info(f"Model accuracy on test data: {score:.2f}")

# Additional metrics
f1 = f1_score(y_test, predictions, average='weighted')  # Use 'weighted' for multiclass F1 score
conf_matrix = confusion_matrix(y_test, predictions)

tp = np.diag(conf_matrix)
tn = np.sum(conf_matrix) - (np.sum(conf_matrix, axis=0) + np.sum(conf_matrix, axis=1) - tp)
fp = np.sum(conf_matrix, axis=0) - tp
fn = np.sum(conf_matrix, axis=1) - tp
# Log additional metric
fp_rate = fp / (fp + tn)
fn_rate = fn / (fn + tp)

# Log additional metrics
logging.info(f"F1 Score: {f1:.2f}")
logging.info(f"True Negative: {tn}")
logging.info(f"False Positive: {fp}")
logging.info(f"False Negative: {fn}")
logging.info(f"True Positive: {tp}")
logging.info(f"False Positive Rate: {fp_rate:}")
logging.info(f"False Negative Rate: {fn_rate:}")

# Log model parameters
logging.info(f"Model coefficients: {model.coef_}")
logging.info(f"Model intercept: {model.intercept_}")
