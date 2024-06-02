import json
import logging
import requests
import pandas as pd

AIRFLOW_TASK = "airflow.task"
logger = logging.getLogger(AIRFLOW_TASK)


def read_and_serialize(**kwargs):

    file_path = kwargs["file_path"]
    with open(file_path, 'r') as file:
        data = json.load(file)
    serialized_data = json.dumps(data)
    logger.info(f"Serialized Data: {serialized_data}")


def process_file(file_path, output_path, **kwargs):
    df = pd.read_csv(file_path)
    df.fillna(1, inplace=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Processed file saved to {output_path}")


def file_operation(file_path, **kwargs):
    with open(file_path, 'r') as file:
        data = file.read()
    logger.info(f"Read data: {data}")


def make_http_request(url, **kwargs):
    response = requests.get(url)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")
