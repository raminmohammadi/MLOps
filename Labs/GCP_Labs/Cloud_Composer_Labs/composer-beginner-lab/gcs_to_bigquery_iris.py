from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
import os

# Replace with your actual bucket name.
# This is the bucket where you store the Iris dataset not the bucket where you store the DAGs.
BUCKET_NAME = 'composer-demo-bucket'
IRIS_FILE_NAME = 'iris.data'

# Using the project ID from the Airflow environment
PROJECT_ID = os.environ.get('GCP_PROJECT')

default_args = {
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5), # Here you pass a time duration (timedelta) object
}

dag = DAG(
    'gcs_to_bigquery_iris',
    default_args=default_args,
    description='Load Iris dataset from GCS to BigQuery',
    schedule_interval=timedelta(days=1), # The same as retry_delay parameter, timedelta object
)

def check_file_exists(**kwargs):
    gcs_hook = GCSHook()
    if gcs_hook.exists(BUCKET_NAME, IRIS_FILE_NAME):
        return 'file_exists_dummy'
    else:
        return 'download_iris_data'

check_file_task = BranchPythonOperator(
    task_id='check_file_exists',
    python_callable=check_file_exists,
    dag=dag,
)

download_iris_data = BashOperator(
    task_id='download_iris_data',
    bash_command=f'curl https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data -o /tmp/{IRIS_FILE_NAME}',
    dag=dag,
)

def upload_to_gcs(**kwargs):
    gcs_hook = GCSHook()
    gcs_hook.upload(BUCKET_NAME, IRIS_FILE_NAME, f'/tmp/{IRIS_FILE_NAME}')

upload_to_gcs_task = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_to_gcs,
    dag=dag,
)

file_exists_dummy = DummyOperator(
    task_id='file_exists_dummy',
    dag=dag,
)

load_to_bigquery = GCSToBigQueryOperator(
    task_id='gcs_to_bigquery',
    bucket=BUCKET_NAME,
    source_objects=[IRIS_FILE_NAME],
    destination_project_dataset_table=f'{PROJECT_ID}.mlops_lab.iris_dataset',
    schema_fields=[
        {'name': 'sepal_length', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'sepal_width', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'petal_length', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'petal_width', 'type': 'FLOAT', 'mode': 'NULLABLE'},
        {'name': 'species', 'type': 'STRING', 'mode': 'NULLABLE'},
    ],
    write_disposition='WRITE_TRUNCATE',
    source_format='CSV',
    field_delimiter=',',
    trigger_rule='TriggerRule.ONE_SUCCESS',
    dag=dag,
)

check_file_task >> [download_iris_data, file_exists_dummy]
download_iris_data >> upload_to_gcs_task >> load_to_bigquery
file_exists_dummy >> load_to_bigquery