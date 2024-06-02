from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
from dag_functions import (
    file_operation,
    make_http_request,
    read_and_serialize,
    process_file,
)
import logging

AIRFLOW_TASK = "airflow.task"
logger = logging.getLogger(AIRFLOW_TASK)

default_args = {
    'owner': 'Aadit',
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
    python_callable=read_and_serialize,
    op_kwargs={'file_path': '/path/to/your/file.json'},
    dag=dag_1,
)

process_task = PythonOperator(
    task_id='process_file',
    python_callable=process_file,
    op_kwargs={
        'file_path': '/path/to/your/input.csv',
        'output_path': '/path/to/your/output.csv',
    },
    dag=dag_1,
)

file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    fs_conn_id='fs_default',
    filepath='/path/to/your/file.csv',
    poke_interval=10,
    timeout=300,
    dag=dag_1,
)

read_serialize_task >> process_task >> file_sensor_task


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
    op_kwargs={'file_path': '/path/to/your/file.txt'},
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
)

# EmailOperator: Sends an email
email_task = EmailOperator(
    task_id='email_task',
    to='shah.aadit1@northeastern.com',
    subject='Airflow Task Completed',
    html_content='<p>The Airflow task has been completed successfully.</p>',
    dag=dag_3,
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
start_task >> [bash_task, branch_task]
bash_task >> middle_task >> end_task
branch_task >> email_task >> end_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag_1.cli()
    dag_2.cli()
    dag_3.cli()
