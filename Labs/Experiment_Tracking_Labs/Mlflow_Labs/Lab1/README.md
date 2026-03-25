# MLflow Lab 1 — Experiment Tracking

## Original Lab

| File | Model | Dataset |
|------|-------|---------|
| `linear_regression.py` / `.ipynb` | ElasticNet (alpha=0.5, l1_ratio=0.5) | Red Wine Quality |
| `starter.ipynb` | RandomForestRegressor (n_estimators=100, max_depth=6, max_features=3) | Diabetes |
| `serving.ipynb` | LinearRegression | Diabetes |
| `serving.py` | XGBoost | Iris |

## Changes Made

| File | What Changed |
|------|-------------|
| `linear_regression.py` / `.ipynb` | Model: ElasticNet -> **Ridge** (alpha=1.0). Dataset: red wine -> **white wine**. Split: 75/25 -> **80/20**. Fixed `l2_ratio` typo in print statement. |
| `starter.ipynb` | Model: RandomForestRegressor -> **GradientBoostingRegressor** (n_estimators=200, max_depth=4, learning_rate=0.1) |
| `serving.ipynb` | Model: LinearRegression -> **Lasso** (alpha=0.1). Fixed registered model name from "RandomForest" -> **"LassoDiabetesModel"** |

## Results

### Ridge Regression on White Wine Quality (`linear_regression.py`)

| Metric | Value |
|--------|-------|
| RMSE | 0.7634 |
| MAE | 0.5940 |
| R2 | 0.2475 |

## How to Run

```bash
pip install -r requirements.txt
python linear_regression.py
mlflow ui --port 5001
```

Then open http://127.0.0.1:5001 to view the logged runs, parameters, metrics, and artifacts.
