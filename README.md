## Lab 1 – API with FastAPI

In this lab, I built a FastAPI application to serve ML predictions on the Iris dataset.

### Changes Implemented

- **Added new models**:

  - Random Forest (`rf`)
  - Logistic Regression (`lr`)

- **Extended training script (`train.py`)**

  - Trains and saves three models: Decision Tree, Random Forest, Logistic Regression

- **Created separate prediction functions** in `predict.py`

  - `predict_dt`, `predict_rf`, `predict_lr`

- **New endpoints in `main.py`**

  - `POST /predict/dt` → Decision Tree
  - `POST /predict/rf` → Random Forest
  - `POST /predict/lr` → Logistic Regression

- **Improved response schema**

  - Predictions now return both the **class index** and the **species name** (`setosa`, `versicolor`, `virginica`).
