# wine_pipeline.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import json


def load_data(**kwargs):
    """Load and clean the dataset"""
    import pandas as pd, os

    data_path = os.path.join(os.path.dirname(__file__), "../data/winequality-red.csv")

    # Read semicolon-separated CSV and clean column names
    df = pd.read_csv(data_path, sep=';')
    df.columns = (
        df.columns
        .str.strip()
        .str.replace('"', '')
        .str.replace(' ', '_').str.lower()
    )

    print(" Data loaded ")

    print("Columns:", list(df.columns))
    print("\nMissing values per column:\n", df.isna().sum())

    # Log summary statistics
    print("\n=== Summary Statistics ===")
    print(df.describe())

    return df.to_json()



def preprocess_data(**kwargs):
    """Preprocess data (encode categorical features, separate X/y)"""
    import pandas as pd, json, os
    ti = kwargs['ti']
    data_json = ti.xcom_pull(task_ids='load_data')
    df = pd.DataFrame(json.loads(data_json))


    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    if 'color' in df.columns:
        df['color'] = df['color'].map({'red': 0, 'white': 1}).fillna(0)

    if 'quality' not in df.columns:
        raise KeyError(f"'quality' not found. Found columns: {list(df.columns)}")

    X = df.drop(columns=['quality'])
    y = df['quality']

    os.makedirs("data_temp", exist_ok=True)
    X.to_csv("data_temp/X.csv", index=False)
    y.to_csv("data_temp/y.csv", index=False)
    print("Preprocessing complete")


def train_model(**kwargs):
    """Train a Linear Regression model and push evaluation metrics."""
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    import joblib, os

    ti = kwargs["ti"]

    # Read the intermediate data saved by preprocess_data
    X = pd.read_csv("data_temp/X.csv")
    y = pd.read_csv("data_temp/y.csv").squeeze()


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )


    model = LinearRegression()
    model.fit(X_train, y_train)


    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print("Model training completed")
    print(f"🔹 MSE: {mse:.4f}")
    print(f"🔹 R² Score: {r2:.4f}")


    os.makedirs("models", exist_ok=True)
    model_path = "models/wine_quality_model.pkl"
    joblib.dump(model, model_path)
    print(f"💾 Model saved at: {model_path}")

    # Push metrics to XCom (convert to float to avoid numpy serialization issues)
    ti.xcom_push(key="mse", value=float(mse))
    ti.xcom_push(key="r2", value=float(r2))




def finish_pipeline(**kwargs):
    """Final task to log completion and metrics"""
    ti = kwargs['ti']
    mse = ti.xcom_pull(task_ids='train_model', key='mse')
    r2 = ti.xcom_pull(task_ids='train_model', key='r2')

    print("🎉 Workflow complete: Wine Quality model ready!")

    if mse is None or r2 is None:
        print("⚠️ Warning: Could not retrieve metrics from XCom.")
        print("Possible cause: train_model did not push results.")
    else:
        print(f"📊 Final Metrics → MSE: {float(mse):.4f}, R²: {float(r2):.4f}")
