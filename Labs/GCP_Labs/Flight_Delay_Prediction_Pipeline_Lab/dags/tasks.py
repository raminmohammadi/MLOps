import smtplib
from email.mime.text import MIMEText
import logging
import uuid
from airflow.models import Variable
import json
import subprocess
import os
import logging


PROJECT_ID = Variable.get("PROJECT_ID")
REGION = Variable.get("REGION")
GCR_IMAGE_PATH = Variable.get('GCR_IMAGE_PATH')


def send_email(status):
    sender_email = Variable.get('EMAIL_USER')
    receiver_email = Variable.get("RECEIVER_EMAIL")
    password = Variable.get('EMAIL_PASSWORD')

    if status == "success":
        subject = "Airflow DAG Succeeded"
        body = "Hello, your DAG has completed successfully."
    else:
        subject = "Airflow DAG Failed"
        body = "Hello, your DAG has failed. Please check the logs for more details."

    # Create the email headers and content
    email_message = MIMEText(body)
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_email

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
    finally:
        server.quit()


def print_preorder(path, indent=0):
    # Print the current directory or file
    print(' ' * indent + os.path.basename(path))

    # If the current path is a directory, recursively traverse its contents
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            print_preorder(item_path, indent + 2)


# Specify the directory to start from
start_path = '/path/to/start/directory'


def train_model(**kwargs):
    username = kwargs['ti'].xcom_pull(task_ids='get_username')
    script_path = f"/home/{username}/Desktop/modelling-mlops/xgboost-model-v2.py"
    python_command = f"python3 {script_path}"
    subprocess.run(python_command, shell=True, check=True)


def get_latest_image_tag():
    command = f"gcloud container images list-tags {GCR_IMAGE_PATH} --limit=1 --sort-by=~TIMESTAMP --format='get(digest)'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    latest_tag = result.stdout.strip()
    return f"{GCR_IMAGE_PATH}@{latest_tag}"


def create_batch_job(**context):
    latest_image = context['task_instance'].xcom_pull(task_ids='get_latest_image_tag')
    job_name = f"ml-training-job-{uuid.uuid4()}"

    job_config = {
        "name": f"projects/{PROJECT_ID}/locations/{REGION}/jobs/{job_name}",
        "taskGroups": [
            {
                "taskCount": "1",
                "parallelism": "1",
                "taskSpec": {
                    "computeResource": {"cpuMilli": "4000", "memoryMib": "32768"},
                    "runnables": [
                        {
                            "container": {
                                "imageUri": latest_image,
                                "entrypoint": "",
                                "volumes": [],
                            }
                        }
                    ],
                    "volumes": [],
                },
            }
        ],
        "allocationPolicy": {
            "instances": [
                {
                    "policy": {
                        "provisioningModel": "STANDARD",
                        "machineType": "e2-highmem-4",
                    }
                }
            ]
        },
        "logsPolicy": {"destination": "CLOUD_LOGGING"},
    }

    config_path = '/tmp/batch-job-config.json'
    try:
        with open(config_path, 'w') as config_file:
            json.dump(job_config, config_file)
    except Exception as e:
        print(f"Error creating batch job config file: {e}")
        raise

    context['task_instance'].xcom_push(key='config_path', value=config_path.strip())
    context['task_instance'].xcom_push(key='job_name', value=job_name.strip())

    return config_path
