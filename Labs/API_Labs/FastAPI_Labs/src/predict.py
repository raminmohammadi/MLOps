"""
predict.py

Provides a wrapper function predict_data(X) that loads the trained model
and returns predicted class labels for input X.
"""
import os
import joblib
import numpy as np

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "diabetes_model.pkl"))

def predict_data(X):
    """
    Predict the class labels for the input data.
    Args:
        X: array-like of shape (n_samples, n_features)
    Returns:
        numpy array with predicted labels (0/1)
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run src/train.py first.")
    model = joblib.load(MODEL_PATH)
    X_arr = np.asarray(X, dtype=float)
    # Ensure 2D
    if X_arr.ndim == 1:
        X_arr = X_arr.reshape(1, -1)
    y_pred = model.predict(X_arr)
    return y_pred

