from airflow.models.dagrun import DagRun
from airflow.utils.state import State
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template



# Default arguments for DAG
default_args = {
    # 'owner': 'airflow',
    'start_date': datetime.now(),
    'retries': 0 # NUmber of attempts in case of failure
}

# Lets create a Flask API to show sucess or failure of the main dag
app = Flask(__name__)

# Function to check the status of the last DAG run
def check_dag_status():
    dag_id = 'Airflow_Lab2'
    dag_runs = DagRun.find(dag_id=dag_id, state=State.SUCCESS)
    if dag_runs:
        return True
    else:
        return False

# Flask route to handle API request
@app.route('/api')
def handle_api_request():
    if check_dag_status():
        return redirect('/success')
    else:
        return redirect('/failure')
    
# Flask routes
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

# Function to start Flask app
def start_flask_app():
    app.run(host='0.0.0.1', port=5555)

#To address this issue, you can use the TriggerDagRunOperator to trigger a separate DAG once start_flask_API starts the Flask server.
# This new DAG can handle the Flask server's lifecycle independently, allowing the current DAG to proceed with sending the email.

flask_api_dag = DAG('Airflow_Lab2_Flask',
                              default_args=default_args,
                              description='DAG to manage Flask API lifecycle',
                              schedule_interval=None,
                              catchup=False,
                              tags=['Flask_Api']         
)


start_flask_API = PythonOperator(
    task_id = 'start_Flask_API',
    python_callable=start_flask_app,
    dag = flask_api_dag
)

start_flask_API

