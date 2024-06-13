from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator  # Added for flexibility
from datetime import datetime, timedelta

default_args = {
    'owner': 'Ramin Mohammadi', 
    'start_date': datetime(2024, 6, 13),
}

dag = DAG(
    'cloud_composer_tutorial',  
    default_args=default_args,
    description='Introductory DAG for Cloud Composer',
    schedule_interval=None,  # For manual triggering
)

# Task 1: Hello World (BashOperator)
hello_world_task = BashOperator(
    task_id='hello_world',
    bash_command='echo "Hello, Cloud Composer!"',
    dag=dag,
)

# Task 2: Simple Python Task (PythonOperator)
def say_hello():
    print("This is a simple Python task in Airflow.")

say_hello_task = PythonOperator(
    task_id='say_hello',
    python_callable=say_hello,
    dag=dag,
)

# Task Dependencies
hello_world_task >> say_hello_task
