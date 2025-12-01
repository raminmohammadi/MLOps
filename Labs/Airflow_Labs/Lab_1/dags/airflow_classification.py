# dags/airflow_classification.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow import configuration as conf

# Functions from your module (paths & logic live inside classification_lab.py)
from src.classification_lab import (
    load_data,             # returns: pickled pandas DataFrame (bytes)
    data_preprocessing,    # takes: serialized df; returns: {"X_path": "...", "y_path": "..."}
    build_save_model,      # takes: dict with paths; returns: metrics dict
    load_model_predict,    # optional: sample_index kwarg; reads model/X from working_data
)

from src.classification_lab import (
    load_data, data_preprocessing, build_save_model, load_model_predict,
    predict_on_test_csv,   # <-- add this
)

# Allow pickled objects in XCom (since load_data returns a pickled DataFrame)
conf.set("core", "enable_xcom_pickling", "True")

default_args = {
    "owner": "your_name",
    "start_date": datetime(2023, 9, 17),
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="Airflow_Classification",
    default_args=default_args,
    description="Binary classification for credit risk (Logistic Regression)",
    schedule_interval=None,   # trigger manually from the UI
    catchup=False,
    tags=["ml", "classification"],
)

# 1) LOAD CSV  -> returns serialized dataframe via XCom
load_data_task = PythonOperator(
    task_id="load_data_task",
    python_callable=load_data,
    dag=dag,
)

# 2) PREPROCESS -> creates RISK_FLAG, scales features, writes X.pkl/y.pkl
#    You can tweak the labeling rule here (risk_threshold default 0.25)
preprocess_task = PythonOperator(
    task_id="data_preprocessing_task",
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],      # pass serialized df from previous task
    op_kwargs={"risk_threshold": 0.25},   # change to 0.30 etc. if you want
    dag=dag,
)

# 3) TRAIN + SAVE MODEL -> returns metrics dict; also writes metrics.json and classification_model.pkl
train_task = PythonOperator(
    task_id="train_and_save_model_task",
    python_callable=build_save_model,
    op_args=[preprocess_task.output],     # {"X_path": "...", "y_path": "..."}
    dag=dag,
)

# 4) PREDICT (sample) -> loads saved model & X.pkl; logs a human-readable prediction
predict_task = PythonOperator(
    task_id="sample_prediction_task",
    python_callable=load_model_predict,
    op_kwargs={"sample_index": 0},        # change index if you want to test a different row
    dag=dag,
)
predict_on_test_task = PythonOperator(
    task_id="predict_on_test_csv_task",
    python_callable=predict_on_test_csv,
    op_kwargs={"test_path": "/opt/airflow/dags/data/test.csv", "risk_threshold": 0.25},
    dag=dag,
)

train_task >> [predict_task, predict_on_test_task]


# Define dependencies
load_data_task >> preprocess_task >> train_task >> predict_task

if __name__ == "__main__":
    dag.cli()
