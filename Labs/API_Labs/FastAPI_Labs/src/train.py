#!/usr/bin/env python3
import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from data import load_data, split_data

MODEL_OUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "diabetes_model.pkl"))

def fit_model(X_train, y_train):
    """
    Train a Logistic Regression model inside a pipeline (scaling + logistic)
    and return the trained pipeline.
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, solver="liblinear"))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

if __name__ == "__main__":
    # Load and split data
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Train
    model_pipeline = fit_model(X_train, y_train)

    # Evaluate
    preds = model_pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test accuracy: {acc:.4f}")
    print("Classification report:")
    print(classification_report(y_test, preds))

    # Save model
    os.makedirs(os.path.dirname(MODEL_OUT_PATH), exist_ok=True)
    joblib.dump(model_pipeline, MODEL_OUT_PATH)
    print(f"Saved model to {MODEL_OUT_PATH}")

