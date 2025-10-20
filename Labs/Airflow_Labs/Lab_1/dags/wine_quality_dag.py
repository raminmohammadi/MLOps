from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.wine_pipeline import load_data, preprocess_data, train_model, finish_pipeline

default_args = {
    'owner': 'kousik',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='wine_quality_dag',
    default_args=default_args,
    description='Airflow ML pipeline for wine quality prediction',
    start_date=datetime(2025, 10, 20),
    schedule=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id='load_data', python_callable=load_data)
    t2 = PythonOperator(task_id='preprocess_data', python_callable=preprocess_data)
    t3 = PythonOperator(task_id='train_model', python_callable=train_model)
    t4 = PythonOperator(task_id='finish_pipeline', python_callable=finish_pipeline)

    t1 >> t2 >> t3 >> t4
