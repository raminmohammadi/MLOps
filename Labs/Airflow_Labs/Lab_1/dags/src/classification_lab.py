# Labs/Airflow_Labs/Lab_1/dags/src/classification_lab.py

import os
import json
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

# -------- Paths INSIDE the Airflow containers --------
DATA_PATH = "/opt/airflow/dags/data/file.csv"
TEST_DATA_PATH = "/opt/airflow/dags/data/test.csv"

ARTIFACT_DIR = "/opt/airflow/working_data"
MODEL_PATH   = os.path.join(ARTIFACT_DIR, "classification_model.pkl")
METRICS_PATH = os.path.join(ARTIFACT_DIR, "metrics.json")
X_PATH       = os.path.join(ARTIFACT_DIR, "X.pkl")
Y_PATH       = os.path.join(ARTIFACT_DIR, "y.pkl")

# for test-time transforms & predictions
SCALER_PATH            = os.path.join(ARTIFACT_DIR, "scaler.pkl")
FEATURES_PATH          = os.path.join(ARTIFACT_DIR, "feature_columns.json")
NUMERIC_FEATURES_PATH  = os.path.join(ARTIFACT_DIR, "numeric_feature_columns.json")
TEST_PREDICTIONS_PATH  = os.path.join(ARTIFACT_DIR, "test_predictions.csv")

os.makedirs(ARTIFACT_DIR, exist_ok=True)


# 1) LOAD
def load_data():
    df = pd.read_csv(DATA_PATH)
    return pickle.dumps(df)  # small enough for XCom when pickled


# 2) PREPROCESS
def data_preprocessing(serialized_df, risk_threshold: float = 0.25):
    """
    Builds binary label RISK_FLAG = 1 if MINIMUM_PAYMENTS/BALANCE < threshold else 0,
    scales numeric features, and persists:
      - X.pkl / y.pkl
      - scaler.pkl
      - feature_columns.json (order!)
      - numeric_feature_columns.json
    """
    df = pickle.loads(serialized_df)

    # adjust these if your CSV headers differ
    cid_col     = "CUST_ID"
    balance_col = "BALANCE"
    minpay_col  = "MINIMUM_PAYMENTS"

    for col in (balance_col, minpay_col):
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in dataset.")

    df[balance_col] = df[balance_col].fillna(0)
    df[minpay_col]  = df[minpay_col].fillna(0)

    eps = 1e-6
    df["RISK_FLAG"] = (df[minpay_col] / (df[balance_col] + eps) < risk_threshold).astype(int)

    if cid_col in df.columns:
        df = df.drop(columns=[cid_col])

    df = df.dropna(how="any").copy()

    X = df.drop(columns=["RISK_FLAG"])
    y = df["RISK_FLAG"]

    num_cols = X.select_dtypes(include="number").columns.tolist()
    scaler = StandardScaler()
    X_scaled = X.copy()
    if num_cols:
        X_scaled[num_cols] = scaler.fit_transform(X[num_cols])

    # persist training artifacts
    with open(X_PATH, "wb") as fx:
        pickle.dump(X_scaled, fx)
    with open(Y_PATH, "wb") as fy:
        pickle.dump(y, fy)
    with open(SCALER_PATH, "wb") as fs:
        pickle.dump(scaler, fs)
    with open(FEATURES_PATH, "w") as ff:
        json.dump(list(X.columns), ff)
    with open(NUMERIC_FEATURES_PATH, "w") as fn:
        json.dump(num_cols, fn)

    return {"X_path": X_PATH, "y_path": Y_PATH}


# 3) TRAIN
def build_save_model(paths_dict, model_path: str = MODEL_PATH):
    with open(paths_dict["X_path"], "rb") as fx:
        X = pickle.load(fx)
    with open(paths_dict["y_path"], "rb") as fy:
        y = pickle.load(fy)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    metrics = {
        "Accuracy": acc,
        "Precision_high_risk": report["1"]["precision"],
        "Recall_high_risk": report["1"]["recall"],
        "F1_high_risk": report["1"]["f1-score"],
        "Support_high_risk": report["1"]["support"],
    }

    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


# 4) PREDICT (single sample from training split, just for a log demo)
def load_model_predict(model_path: str = MODEL_PATH, sample_index: int = 0):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(X_PATH, "rb") as fx:
        X = pickle.load(fx)

    row = X.iloc[sample_index:sample_index + 1] if hasattr(X, "iloc") else X[sample_index:sample_index + 1]
    pred = model.predict(row)[0]
    label = "High Risk" if pred == 1 else "Low Risk"
    return f"Sample index {sample_index} predicted class: {label}"


# 5) PREDICT ON TEST CSV (batch) + optional metrics if label columns exist
def predict_on_test_csv(
    test_path: str = TEST_DATA_PATH,
    risk_threshold: float = 0.25,
    save_path: str = TEST_PREDICTIONS_PATH,
):
    # load artifacts
    with open(MODEL_PATH, "rb") as fm:
        model = pickle.load(fm)
    with open(SCALER_PATH, "rb") as fs:
        scaler = pickle.load(fs)
    with open(FEATURES_PATH, "r") as ff:
        feature_cols = json.load(ff)
    with open(NUMERIC_FEATURES_PATH, "r") as fn:
        numeric_cols = set(json.load(fn))

    # load test
    df = pd.read_csv(test_path)

    # optional ground-truth for metrics
    y_true = None
    if {"BALANCE", "MINIMUM_PAYMENTS"}.issubset(df.columns):
        eps = 1e-6
        y_true = (
            (df["MINIMUM_PAYMENTS"].fillna(0) / (df["BALANCE"].fillna(0) + eps) < risk_threshold)
            .astype(int)
        )

    # build X with exact training columns
    X_test = df.reindex(columns=feature_cols, fill_value=0).copy()

    # ensure numeric columns are numeric; scale with the saved scaler
    for c in X_test.columns:
        if c in numeric_cols:
            X_test[c] = pd.to_numeric(X_test[c], errors="coerce").fillna(0)
    if numeric_cols:
        nc = [c for c in feature_cols if c in numeric_cols]
        X_test[nc] = scaler.transform(X_test[nc])

    # predict
    y_pred = model.predict(X_test)

    # save predictions (keep CUST_ID if present)
    out = pd.DataFrame({"prediction": y_pred})
    if "CUST_ID" in df.columns:
        out.insert(0, "CUST_ID", df["CUST_ID"].values[: len(out)])
    out.to_csv(save_path, index=False)

    # return summary / metrics for logs
    if y_true is not None and len(y_true) == len(y_pred):
        acc = accuracy_score(y_true, y_pred)
        rep = classification_report(y_true, y_pred, output_dict=True)
        return {
            "Saved": save_path,
            "Test_Accuracy": acc,
            "Test_Precision_high_risk": rep["1"]["precision"],
            "Test_Recall_high_risk": rep["1"]["recall"],
            "Test_F1_high_risk": rep["1"]["f1-score"],
        }
    return f"Saved {len(out)} predictions to {save_path}"
