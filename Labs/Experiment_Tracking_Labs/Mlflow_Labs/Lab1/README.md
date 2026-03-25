# MLflow Lab 1 — Experiment Tracking

This lab demonstrates core MLflow capabilities: experiment tracking, autologging, model logging, model registry, and local model serving.

## Files

| File | Model | Dataset | Description |
|------|-------|---------|-------------|
| `linear_regression.py` | Ridge Regression (alpha=1.0) | White Wine Quality | Manual MLflow logging of params, metrics, and model artifacts |
| `linear_regression.ipynb` | Ridge Regression (alpha=1.0) | White Wine Quality | Notebook version of the above script |
| `starter.ipynb` | GradientBoostingRegressor (n_estimators=200, max_depth=4, lr=0.1) | Diabetes (sklearn) | MLflow autologging, model storage, and model loading |
| `serving.ipynb` | Lasso Regression (alpha=0.1) | Diabetes (sklearn) | End-to-end workflow: train, log, serve, and query a model via REST API |
| `serving.py` | XGBoost | Iris (sklearn) | Demonstrates `pip_requirements` and `extra_pip_requirements` for model logging |

## Setup

```bash
pip install -r requirements.txt
```

## Running

### Linear Regression script

```bash
python linear_regression.py          # defaults: alpha=1.0
python linear_regression.py 0.5      # custom alpha
```

### Notebooks

Open any `.ipynb` file in Jupyter or VS Code and run cells sequentially.

### MLflow UI

After running experiments, launch the tracking UI:

```bash
mlflow ui --port 5001
```

Then open http://127.0.0.1:5001 in a browser to view logged runs, parameters, metrics, and artifacts.

## Changes from Original Lab

- **Model**: ElasticNet replaced with **Ridge** in `linear_regression.py` / `.ipynb`
- **Dataset**: Red wine quality replaced with **white wine quality**
- **Hyperparameters**: alpha changed to 1.0; l1_ratio removed (not applicable to Ridge)
- **Train/test split**: Changed from 75/25 to **80/20**
- **starter.ipynb**: RandomForestRegressor replaced with **GradientBoostingRegressor** (200 trees, depth 4, learning rate 0.1)
- **serving.ipynb**: LinearRegression replaced with **Lasso** (alpha=0.1); fixed mismatched registered model name to **LassoDiabetesModel**
