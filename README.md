# MLOps Coursework Labs

## Lab 1 – API with FastAPI

In this lab, I built a **FastAPI application** to serve ML predictions on the Iris dataset.

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

---

## Lab 2 – Orchestration with Airflow

In this lab, I built an **Apache Airflow DAG** to orchestrate a machine learning workflow for clustering.

### Changes Implemented

- **Extended pipeline beyond KMeans**

  - Original DAG used **KMeans clustering** only.
  - Added a new **Gaussian Mixture Model (GMM)** branch to compare results.

- **Improved outputs**

  - Both KMeans and GMM predictions are now **saved to CSV files** in the `working_data` directory:
    - `predictions_kmeans.csv`
    - `predictions_gmm.csv`
  - These files contain the original test data with predicted cluster labels.

- **Task design in Airflow**
  - Data load → Preprocessing → **Branch into KMeans & GMM**
  - Each branch trains, saves the model, runs predictions, and stores outputs.
  - Results can be inspected from both **XComs** and saved CSVs.

### DAG Graph

Here is a snapshot of the Airflow DAG pipeline:

![Airflow DAG Graph](airflow_lab.png)

---
