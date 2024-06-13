from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from datetime import datetime, timedelta
from dag_functions import (
    file_operation,
    make_http_request,
    process_file,
    read_and_serialize_return,
    log_file_sensor_output,
    final_task,
)
import logging

AIRFLOW_TASK = "airflow.task"
BUCKET_NAME = "your_bucket_name/your_data_folder_name/"
OUTPUT_PATH = "your_bucket_name/your_data_folder_name/dag_processed_file.csv"
logger = logging.getLogger(AIRFLOW_TASK)

default_args = {
    'owner': 'owner name',
    'start_date': datetime(2023, 9, 17),
    'retries': 0,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5),  # Delay before retries
}

dag_1 = DAG(
    'dag_1_parameterize',
    default_args=default_args,
    description='DAG to parameterize file path, process file, and use FileSensor',
    schedule_interval=None,
    catchup=False,
)

read_serialize_task = PythonOperator(
    task_id='read_and_serialize',
    python_callable=read_and_serialize_return,
    op_kwargs={
        'file_path': OUTPUT_PATH
    },
    dag=dag_1,
)

process_task = PythonOperator(
    task_id='process_file',
    python_callable=process_file,
    op_kwargs={
        'output_path': OUTPUT_PATH,
    },
    provide_context=True,
    dag=dag_1,
)

# File sensor task to check for the processed file's existence
file_sensor_task = GCSObjectExistenceSensor(
    task_id='file_sensor_task',
    bucket=BUCKET_NAME,
    object='data/dag_processed_file.csv',
    poke_interval=10,
    timeout=300,
    dag=dag_1,
    on_success_callback=log_file_sensor_output,
    on_failure_callback=log_file_sensor_output,
)

# Final task to execute after the file sensor task
final_processing_task = PythonOperator(
    task_id='final_processing_task',
    python_callable=final_task,
    op_kwargs={
        'output_path': OUTPUT_PATH,
    },
    dag=dag_1,
)


read_serialize_task >> process_task >> file_sensor_task >> final_processing_task

dag_2 = DAG(
    'dag_file_and_http',
    default_args=default_args,
    description='DAG for file operations and HTTP request',
    schedule_interval=None,
    catchup=False,
)

file_op_task = PythonOperator(
    task_id='file_operation',
    python_callable=file_operation,
    op_kwargs={'file_path': OUTPUT_PATH},
    dag=dag_2,
)

http_request_task = PythonOperator(
    task_id='http_request',
    python_callable=make_http_request,
    op_kwargs={'url': 'https://jsonplaceholder.typicode.com/todos/1'},
    dag=dag_2,
)

file_op_task >> http_request_task

### DAG 3: Task Dependencies

dag_3 = DAG(
    'dag_3_dependencies',
    default_args=default_args,
    description='DAG to demonstrate task dependencies',
    schedule_interval=None,
    catchup=False,
)

# DummyOperator: Used for grouping and branching logic
start_task = DummyOperator(
    task_id='start_task',
    dag=dag_3,
)

# BashOperator: Runs a simple bash command
bash_task = BashOperator(
    task_id='bash_task',
    bash_command='echo "This is a bash command"',
    dag=dag_3,
)

# PythonOperator: Runs a Python callable
middle_task = PythonOperator(
    task_id='middle_task',
    python_callable=lambda: logger.info("Middle Task"),
    dag=dag_3,
    trigger_rule='all_done',  # Execute regardless of the upstream task's status
)

# DummyOperator: Used for grouping and branching logic
branch_task = DummyOperator(
    task_id='branch_task',
    dag=dag_3,
)

# PythonOperator: Runs a Python callable
end_task = PythonOperator(
    task_id='end_task',
    python_callable=lambda: logger.info("End Task"),
    dag=dag_3,
)

# Set task dependencies

"""
The task executes with the following dependencies:

- `start_task`: Initiates the workflow and triggers two parallel tasks.
- `bash_task`: Executes a bash script (or a set of operations) and passes the result to `middle_task`.
- `branch_task`: Executes an independent task (or a set of operations).
- `middle_task`: Processes the output of `bash_task`.
- `end_task`:  Finalizes the workflow by consuming the results of `middle_task` and `branch_task`.

The dependency structure ensures that:
    - `bash_task` and `branch_task` run concurrently.
    - `middle_task` depends on the completion of `bash_task`.
    - `end_task` waits for both `middle_task` and `branch_task` to finish.

This parallel execution can optimize the overall runtime, especially when tasks are I/O bound or computationally independent.
"""

start_task >> [bash_task, branch_task]
bash_task >> middle_task >> end_task
branch_task >> end_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag_1.cli()
    dag_2.cli()
    dag_3.cli()
