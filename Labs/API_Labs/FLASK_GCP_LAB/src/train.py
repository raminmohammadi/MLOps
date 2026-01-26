import os
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def run_training():
    # 1. Load dataset (Iris)
    iris = load_iris()
    X = iris.data   # shape (150, 4)
    y = iris.target # 0,1,2 classes

    # 2. Train / test split (for sanity)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Train a model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 4. Quick eval just so we know it learned
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {acc:.3f}")

    # 5. Make sure model/ directory exists
    os.makedirs("model", exist_ok=True)

    # 6. Save model to model/model.pkl
    joblib.dump(model, "model/model.pkl")
    print("Saved trained model to model/model.pkl")

if __name__ == "__main__":
    run_training()