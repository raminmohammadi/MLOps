from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from src.model_development import load_data, load_model, build_model, data_preprocessing
from airflow import configuration as conf
from airflow.operators.email import EmailOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

# Enable pickle support for XCom
conf.set('core', 'enable_xcom_pickling', 'True')

# Default arguments for DAG
default_args = {
    'start_date': datetime.now(),
    'retries': 0  # Number of retry attempts
}


# Create DAG instance
dag = DAG(
    'Airflow_Lab2',
    default_args=default_args,
    description='Airflow-Lab2 DAG Description',
    schedule_interval='*/1 * * * *',  # Every minute
    catchup=False,  # Disable catchup
    tags=['example'],
    owner_links={"Ramin Mohammadi": "https://github.com/raminmohammadi/MLOps/"} # Automatic setting for the DAG - Not functional 
)

# Task definitions - Manual Setting as a function
owner_task = BashOperator(
    task_id="task_using_linked_owner",
    bash_command="echo 1",
    owner="Ramin Mohammadi",
    dag=dag
)

send_email = EmailOperator(
    task_id='send_email',
    to='rey.mhmmd@gmail.com',
    subject='Notification from Airflow',
    html_content='<p>This is a notification email sent from Airflow.</p>',
    dag=dag
)

load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag
)

data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],  # Pass output from previous task
    dag=dag
)


def separate_data_outputs(**kwargs):
    ti = kwargs['ti']
    X_train, X_test, y_train, y_test = ti.xcom_pull(task_ids='data_preprocessing_task')
    return X_train, X_test, y_train, y_test


separate_data_outputs_task = PythonOperator(
    task_id='separate_data_outputs_task',
    python_callable=separate_data_outputs,
    dag=dag
)

build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],
    dag=dag
)

load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],
    dag=dag
)

TriggerDagRunOperator = TriggerDagRunOperator(
    task_id='my_trigger_task',
    trigger_rule=TriggerRule.ALL_DONE,
    trigger_dag_id='Airflow_Lab2_Flask',
    dag=dag
)

# Set task dependencies
owner_task >> load_data_task >> data_preprocessing_task >> separate_data_outputs_task >> build_save_model_task >> load_model_task >> send_email >> TriggerDagRunOperator
