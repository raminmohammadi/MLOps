from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

from dags.tasks import (
    create_batch_job,
    get_latest_image_tag,
    send_email,
)

REGION = Variable.get("REGION")
PROJECT_ID = Variable.get("PROJECT_ID")
MODEL_BUCKET_NAME = Variable.get("MODEL_BUCKET_NAME")
MODEL_PATH = Variable.get("MODEL_PATH")
MODEL_FILE = Variable.get("MODEL_FILE")

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'batch_job_deployment',
    default_args=default_args,
    description='A DAG to create, run, and delete a Google Batch job',
    schedule_interval=None,  # Change as required
)

get_latest_image_tag_task = PythonOperator(
    task_id='get_latest_image_tag',
    python_callable=get_latest_image_tag,
    dag=dag,
)

create_batch_job_task = PythonOperator(
    task_id='create_batch_job',
    python_callable=create_batch_job,
    provide_context=True,
    dag=dag,
)

monitor_gcs_file_task = GCSObjectExistenceSensor(
    task_id='monitor_gcs_file',
    bucket=MODEL_BUCKET_NAME,
    object='models/model.pkl',
    timeout=1200,  # 20 minutes
    poke_interval=60,  # Check every minute
    dag=dag,
)

submit_batch_job_task = BashOperator(
    task_id='submit_batch_job',
    bash_command="""
        config_path="{{ task_instance.xcom_pull(task_ids='create_batch_job', key='return_value') }}"
        job_name="{{ task_instance.xcom_pull(task_ids='create_batch_job', key='job_name') }}"
        gcloud batch jobs submit $job_name --location={{ var.value.REGION }} --config=$config_path
    """,
    dag=dag,
)

delete_batch_job_task = BashOperator(
    task_id='delete_batch_job',
    bash_command="""
        job_name="{{ task_instance.xcom_pull(task_ids='create_batch_job', key='job_name') }}"
        gcloud batch jobs delete $job_name --location={{ var.value.REGION }} --quiet
    """,
    dag=dag,
)

# Define success and failure email tasks
send_success_email = PythonOperator(
    task_id='send_success_email',
    python_callable=send_email,
    op_args=['success'],
    trigger_rule='all_success',
    dag=dag,
)

send_failure_email = PythonOperator(
    task_id='send_failure_email',
    python_callable=send_email,
    op_args=['failure'],
    trigger_rule='one_failed',
    dag=dag,
)

# Final dummy task to ensure all previous tasks are complete before sending email
end_task = DummyOperator(
    task_id='end',
    dag=dag,
)


"""
This section of the DAG defines the dependencies and the flow of tasks. 

Task Definitions:
1. get_latest_image_tag_task: Retrieves the latest Docker image tag for the batch job.
2. create_batch_job_task: Creates the configuration for the Google Batch job.
3. submit_batch_job_task: Submits the batch job to Google Cloud Batch for execution.
4. monitor_gcs_file_task: Monitors the batch job until it completes successfully or fails.
5. delete_batch_job_task: Deletes the batch job configuration after monitoring is complete, whether successful or not. It is dependent on the completion of monitor_batch_job_task.
6. end_task: A dummy task that signifies the end of the primary workflow. Both deploy_model and monitor_batch_job_task converge here.
7. send_success_email: Sends a success email notification. It is triggered if the end_task completes successfully.
8. send_failure_email: Sends a failure email notification. It is triggered if the end_task fails.

Dependencies:
- get_latest_image_tag_task >> create_batch_job_task >> submit_batch_job_task >> monitor_batch_job_task
- monitor_gcs_file_task >> delete_batch_job_task
- monitor_gcs_file_task >> end_task
- end_task >> send_success_email
- end_task >> send_failure_email
"""

# Define task dependencies
(
    get_latest_image_tag_task
    >> create_batch_job_task
    >> submit_batch_job_task
    >> monitor_gcs_file_task
)
monitor_gcs_file_task >> delete_batch_job_task
monitor_gcs_file_task >> end_task
end_task >> send_success_email
end_task >> send_failure_email
