from airflow import DAG
from datetime import datetime, timedelta
from ..plugins.custom_operators.ml_operators import (
    MLModelTrainOperator,
    ModelDeployOperator,
)


default_args = {
    'owner': 'mlops',
    'start_date': datetime.now() - timedelta(days=1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'retries': 1,
}

dag = DAG(
    'model_training_and_deployment',
    default_args=default_args,
    description='Train and deploy machine learning models',
    schedule_interval=None,  # This is manually triggered by the first DAG
    catchup=False,
)

# Task 1: Train Model
train_model = MLModelTrainOperator(
    task_id='train_model',
    data_path='gs://your-bucket/data/Clean_Energy_Consumption.csv',
    save_path='gs://your-bucket/models/',
    dag=dag,
)

# Task 2: Deploy Model
deploy_model = ModelDeployOperator(
    task_id='deploy_model',
    model_path='gs://your-bucket/models/model.pkl',
    deployment_target='production',
    dag=dag,
)

train_model >> deploy_model
