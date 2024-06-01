from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from src.model_development import load_data, load_model, build_model, data_preprocessing
from airflow import configuration as conf
from airflow.operators.email_operator import EmailOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

#Enable pickle support for XCom, allowing data to be passed between tasks
conf.set('core', 'enable_xcom_pickling', 'True')

# Default arguments for DAG
default_args = {
    # 'owner': 'airflow',
    'start_date': datetime.now(),
    'retries': 0 # NUmber of attempts in case of failure
}

# Now create the main Dag

# Define function to notify failure or sucess via an email
def notify_success(context):
    success_email = EmailOperator(
        task_id='success_email',
        to='rey.mhmmd@gmail.com',
        subject='Success Notification from Airflow',
        html_content='<p>The task succeeded.</p>',
        dag=context['dag']
    )
    success_email.execute(context=context)

def notify_failure(context):
    failure_email = EmailOperator(
        task_id='failure_email',
        to='rey.mhmmd@gmail.com',
        subject='Failure Notification from Airflow',
        html_content='<p>The task failed.</p>',
        dag=context['dag']
    )
    failure_email.execute(context=context)


# Create DAG instance
dag  = DAG('Airflow_Lab2', 
           default_args=default_args,
           description='Aiflow-Lab2 DAG Description',
           schedule_interval='1 * * * *',
           catchup=False, #The scheduler, by default, will kick off a DAG Run for any data interval that has not been run since the last data interval (or has been cleared). This concept is called Catchup.
           tags=['example'],
           owner_links={"Ramin Mohammadi": "https://github.com/raminmohammadi/MLOps/"}         
)

# define a task using this owner, and the owner in the DAGs view will link to the specified address.
owner_task = BashOperator(task_id="task_using_linked_owner",
                          bash_command="echo 1",
                          owner="Ramin Mohammadi")



# Define the email task
send_email = EmailOperator(
    task_id='send_email',
    to='rey.mhmmd@gmail.com',    # Email address of the recipient
    subject='Notification from Airflow',
    html_content='<p>This is a notification email sent from Airflow.</p>',
    dag=dag,
    on_failure_callback=notify_failure,
    on_success_callback=notify_success
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




TriggerDagRunOperator = TriggerDagRunOperator(dag=dag,
                                              task_id='my_trigger_task',
                                              trigger_rule=TriggerRule.ALL_DONE,
                                              trigger_dag_id='Airflow_Lab2_Flask')


# Set task dependencies
owner_task >> load_data_task >> data_preprocessing_task >> separate_data_outputs_task >> build_save_model_task >> load_model_task >> send_email >> TriggerDagRunOperator



# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.cli()
