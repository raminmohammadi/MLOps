# MLOps Coursework Labs

## Lab 1 – (API Lab) API with FastAPI

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

## Lab 2 – (Airflow Lab) Orchestration with Airflow

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

## Lab 3 – (Docker Lab) Flask Deployment and Model Enhancement

In this lab, I extended the **Dockerized Flask application** from previous work to serve multiple models and improve observability.

### Changes Implemented

- **Added a `/health` endpoint**

  - Simple `GET /health` route returning `{"status": "ok"}` for container health checks.
  - Used to confirm the app is running successfully inside Docker.

- **Introduced a new model (K-Nearest Neighbors)**

  - `model_training.py` now trains and saves both:
    - Logistic Regression (`my_model.pkl`)
    - KNN Classifier (`knn_model.pkl`)
  - Both models share a common `StandardScaler` to ensure consistent preprocessing.

- **Added a new prediction endpoint**

  - `GET` / `POST /predict` → serves predictions using the Logistic Regression model.
  - `GET` / `POST /predict_knn` → serves predictions using the new KNN model.
  - Both endpoints can return JSON responses or render an HTML input form.

- **Updated Docker setup**

  - Multi-stage Dockerfile:
    - Stage 1 trains the models.
    - Stage 2 serves predictions through Flask.
  - Model artifacts (`.pkl` files and `scaler.pkl`) are copied from the training stage into the serving image.
  - CMD updated to run `main.py` automatically at container startup.

### 🐳 How to Build and Run (Lab 3)

**Build the image**

```bash
docker build -t app .
```

---
