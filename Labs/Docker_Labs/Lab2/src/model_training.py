# model_training.py
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np
import random

# Reproducibility
random.seed(42)
np.random.seed(42)

if __name__ == "__main__":
    # 1) Load data
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    # 2) Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3) Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 4) Train models
    # 4a) Logistic Regression
    logreg = LogisticRegression(max_iter=1000)
    logreg.fit(X_train, y_train)
    logreg_acc = logreg.score(X_test, y_test)

    # 4b) K-Nearest Neighbors
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    knn_acc = knn.score(X_test, y_test)

    # 5) Save artifacts
    joblib.dump(logreg, "my_model.pkl")
    joblib.dump(knn, "knn_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

    # 6) Report
    print(f"LogReg test accuracy: {logreg_acc:.4f}")
    print(f"KNN    test accuracy: {knn_acc:.4f}")
    print("Saved: my_model.pkl, knn_model.pkl, scaler.pkl")
