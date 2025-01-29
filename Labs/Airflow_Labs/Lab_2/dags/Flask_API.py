from airflow.models.dagrun import DagRun
from airflow.utils.state import State
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template
import time


# Default arguments for DAG
default_args = {
    # 'owner': 'airflow',
    'start_date': datetime.now(),
    'retries': 0 # NUmber of attempts in case of failure
}


# Lets create a Flask API to show success or failure of the main dag
app = Flask(__name__)

# Root route to return a simple message
@app.route('/')
def index():
    if check_dag_status():
        return redirect('/success')
    else:
        return redirect('/failure')


# Function to check the status of the last DAG run
def check_dag_status():
    dag_id = 'Airflow_Lab2'
    dag_runs = DagRun.find(dag_id=dag_id, state=State.SUCCESS)
    if dag_runs:
        return True
    else:
        return False

# Flask routes for success and failure
@app.route('/success')
def success():# -> Any:
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')


# Function to start Flask app
def start_flask_app():
    # Start the Flask app directly here
    app.run(host='0.0.0.0', port=5555)

# Create the DAG instance
flask_api_dag = DAG('Airflow_Lab2_Flask',
                    default_args=default_args,
                    description='DAG to manage Flask API lifecycle',
                    schedule_interval=None,
                    catchup=False,
                    tags=['Flask_Api'])

# Start the Flask API server task
start_flask_API = PythonOperator(
    task_id='start_Flask_API',
    python_callable=start_flask_app,
    dag=flask_api_dag
)


# Set task dependencies
start_flask_API

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    start_flask_API.cli() #Automatic Startup
