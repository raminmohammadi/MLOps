# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.lab import (
    load_data, data_preprocessing,
    build_save_model, load_model_elbow,
    build_save_gmm, load_model_gmm  # NEW IMPORTS
)

from airflow import configuration as conf

# Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

# Define default arguments for your DAG
default_args = {
    'owner': 'Yashi_Chawla',
    'start_date': datetime(2025, 1, 15),
    'retries': 0,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5),  # Delay before retries
}

# Create a DAG instance named 'Airflow_Lab1' with the defined default arguments
dag = DAG(
    'Airflow_Lab1',
    default_args=default_args,
    description='Dag example for Lab 1 of Airflow series with KMeans and GMM',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)

# ---------------- Existing KMeans path ---------------- #

# Task to load data, calls the 'load_data' Python function
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)

# Task to perform data preprocessing, depends on 'load_data_task'
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)

# Task to build and save a KMeans model
build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, "model_kmeans.sav"],
    dag=dag,
)

# Task to load a KMeans model and run elbow method
load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=["model_kmeans.sav", build_save_model_task.output],
    dag=dag,
)

# ---------------- NEW GMM path ---------------- #

# Task to build and save a GMM model
build_save_gmm_task = PythonOperator(
    task_id='build_save_gmm_task',
    python_callable=build_save_gmm,
    op_args=[data_preprocessing_task.output, "model_gmm.sav"],
    dag=dag,
)

# Task to load a GMM model and predict clusters
load_model_gmm_task = PythonOperator(
    task_id='load_model_gmm_task',
    python_callable=load_model_gmm,
    op_args=["model_gmm.sav"],
    dag=dag,
)

# ---------------- Task dependencies ---------------- #

# Common preprocessing, then branch into KMeans and GMM
data_preprocessing_task >> [build_save_model_task, build_save_gmm_task]
build_save_model_task >> load_model_task
build_save_gmm_task >> load_model_gmm_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()