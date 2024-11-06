from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import aiplatform
from datetime import datetime, timedelta
import pandas as pd
from airflow.utils.dates import days_ago
from Lab3.dags.dag_functions import fetch_and_predict

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'model_prediction_dag',
    default_args=default_args,
    description='Fetch data from deployed model on Vertex AI and make predictions',
    schedule_interval=None,
    catchup=False,
)

fetch_and_predict_task = PythonOperator(
    task_id='fetch_and_predict',
    python_callable=fetch_and_predict,
    params={
        'project_id': '{your-project-id}',
        'endpoint_id': '{your-endpoint-id}',
        'instances': [
            # Add your instance data here for predictions
        ],
    },
    dag=dag,
)

fetch_and_predict_task
