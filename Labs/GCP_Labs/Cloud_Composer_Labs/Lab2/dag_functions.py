import json
import logging
import requests
import pandas as pd
import io
from airflow.providers.google.cloud.hooks.gcs import GCSHook

AIRFLOW_TASK = "airflow.task"
logger = logging.getLogger(AIRFLOW_TASK)


def read_and_serialize(**kwargs):
    gcs_hook = GCSHook()
    file_path = kwargs["file_path"]
    bucket_name = file_path.split("/")[0]  # Extract bucket name
    object_name = "/".join(file_path.split("/")[1:])
    file_content = gcs_hook.download(
        bucket_name=bucket_name, object_name=object_name
    ).decode('utf-8')

    logger.info(f"File content: {file_content}")  # Log the file content for debugging
    try:
        df = pd.read_csv(io.StringIO(file_content))
        serialized_data = df.to_json()
        logger.info(f"Serialized Data: {serialized_data}")
        return serialized_data  # Return serialized data for XCom usage
    except Exception as e:
        logger.error(f"Failed to process CSV: {e}")
        raise


def read_and_serialize_return(**kwargs):
    return read_and_serialize(**kwargs)


def process_file(**kwargs):
    ti = kwargs['ti']
    serialized_data = ti.xcom_pull(task_ids='read_and_serialize')
    df = pd.read_json(serialized_data)

    df.fillna(1, inplace=True)
    output_path = kwargs['output_path']

    gcs_hook = GCSHook()
    bucket_name = output_path.split("/")[0]  # Extract bucket name
    object_name = "/".join(output_path.split("/")[1:])

    with io.StringIO() as temp_file:
        df.to_csv(temp_file, index=False)
        temp_file.seek(0)
        gcs_hook.upload(
            bucket_name=bucket_name, object_name=object_name, data=temp_file.read()
        )

    logger.info(f"Processed file saved to {output_path}")


def file_operation(**kwargs):
    gcs_hook = GCSHook()
    file_path = kwargs["file_path"]
    bucket_name = file_path.split("/")[0]  # Extract bucket name
    object_name = "/".join(file_path.split("/")[1:])
    file_content = gcs_hook.download(
        bucket_name=bucket_name, object_name=object_name
    ).decode('utf-8')

    logger.info(f"Read data: {file_content}")


def make_http_request(url):
    response = requests.get(url)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")
