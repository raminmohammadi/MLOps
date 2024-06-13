# dag_tasks.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow.utils.dates import days_ago
from datetime import timedelta
from functions import (
    download_and_serialize_data,
    clean_data,
    upload_cleaned_data,
    bigquery_analysis,
)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'data_processing_and_bigquery_integration',
    default_args=default_args,
    description='Process data and load into BigQuery',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

download_serialize_task = PythonOperator(
    task_id='download_and_serialize',
    python_callable=download_and_serialize_data,
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id='clean_data', python_callable=clean_data, dag=dag
)

upload_cleaned_task = PythonOperator(
    task_id='upload_cleaned_data', python_callable=upload_cleaned_data, dag=dag
)

file_sensor_task = GCSObjectExistenceSensor(
    task_id='check_file_in_gcs',
    bucket='us-central1-composer-env-05cbc839-bucket',
    object='data/Clean_Energy_Consumption.csv',
    dag=dag,
)

load_to_bigquery_task = GCSToBigQueryOperator(
    task_id='load_to_bigquery',
    bucket='us-central1-composer-env-05cbc839-bucket',
    source_objects=['data/Clean_Energy_Consumption.csv'],
    destination_project_dataset_table='your-project.your-dataset.your_table',
    write_disposition='WRITE_TRUNCATE',
    skip_leading_rows=1,
    dag=dag,
)

bigquery_analysis_task = PythonOperator(
    task_id='bigquery_analysis', python_callable=bigquery_analysis, dag=dag
)

(
    download_serialize_task
    >> clean_data_task
    >> upload_cleaned_task
    >> file_sensor_task
    >> load_to_bigquery_task
    >> bigquery_analysis_task
)
