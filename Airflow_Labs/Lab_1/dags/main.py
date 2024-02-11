from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.airflow_github import load_data, load_model, build_model, data_preprocessing
from airflow import configuration as conf


#Define Github repo, owner and endpoint
github_repo = "raminmohammadi/Airflow_github"
owner, repo = github_repo.split("/")
endpoint = f"repos/{owner}/{repo}/issues"

#Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

# Default arguments for DAG
default_args = {
    'owner': owner,
    'start_date': datetime.now(),
    'retries': 0 # NUmber of attempts in case of failure
}

# Create DAG instance
dag  = DAG('Airflow_Github', 
           default_args=default_args,
           description='Aiflow-Github DAG Description',
           schedule_interval=None,
           catchup=False          
)

# Define PythonOperators for each function

# Task to load data, calls the 'load_data' Python function

load_data_task = PythonOperator(
    task_id = 'load_data_task',
    python_callable=load_data,
    provide_context=True,
    dag = dag
)

# Task to perform data preprocessing, depends on 'load_data_task'
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],  # Pass the output of 'load_data_task' as an argument
    dag=dag,
)

# Define a function to separate data outputs
def separate_data_outputs(**kwargs):
    ti = kwargs['ti']
    X_train, X_test, y_train, y_test = ti.xcom_pull(task_ids='data_preprocessing_task')
    return X_train, X_test, y_train, y_test

# Task to execute the 'separate_data_outputs' function
separate_data_outputs_task = PythonOperator(
    task_id='separate_data_outputs_task',
    python_callable=separate_data_outputs,
    provide_context=True,
    dag=dag,
)

# Task to build and save a model, depends on 'separate_data_outputs_task'
build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],  # Pass the output of 'separate_data_outputs_task'
    provide_context=True,
    dag=dag,
)

# Task to load a model using the 'load_model' function, depends on 'build_save_model_task'
load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model,
    op_args=[separate_data_outputs_task.output, "model.sav"],  # Pass the output of 'separate_data_outputs_task'
    dag=dag,
)

# Set task dependencies
load_data_task >> data_preprocessing_task >> separate_data_outputs_task >> build_save_model_task >> load_model_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()