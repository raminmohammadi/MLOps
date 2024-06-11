import json
import logging
import requests
import pandas as pd
import io
from airflow.providers.google.cloud.hooks.gcs import GCSHook

AIRFLOW_TASK = "airflow.task"
logger = logging.getLogger(AIRFLOW_TASK)


def read_and_serialize(**kwargs):
    """
    Reads a CSV file from Google Cloud Storage, serializes it to JSON, and returns the serialized data.

    Args:
        kwargs: Additional keyword arguments containing 'file_path' which is the path to the file in GCS.

    Returns:
        str: Serialized data in JSON format.

    Raises:
        Exception: If there is an error in reading or processing the CSV file.
    """
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
    """
    Wrapper function to call read_and_serialize with keyword arguments.

    Args:
        kwargs: Additional keyword arguments to be passed to read_and_serialize.

    Returns:
        str: Serialized data in JSON format.
    """
    return read_and_serialize(**kwargs)


def process_file(**kwargs):
    """
    Processes the serialized data pulled from XCom, fills NaN values, and uploads the processed file to GCS.

    Args:
        kwargs: Additional keyword arguments containing 'ti' for task instance and 'output_path' for the GCS path to save the processed file.

    Raises:
        Exception: If there is an error in uploading the processed file to GCS.
    """
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
    """
    Reads a file from GCS and logs its content.

    Args:
        kwargs: Additional keyword arguments containing 'file_path' which is the path to the file in GCS.
    """
    gcs_hook = GCSHook()
    file_path = kwargs["file_path"]
    bucket_name = file_path.split("/")[0]  # Extract bucket name
    object_name = "/".join(file_path.split("/")[1:])
    file_content = gcs_hook.download(
        bucket_name=bucket_name, object_name=object_name
    ).decode('utf-8')

    logger.info(f"Read data: {file_content}")


def make_http_request(url):
    """
    Makes an HTTP GET request to the specified URL and logs the response.

    Args:
        url (str): The URL to make the HTTP request to.

    Raises:
        Exception: If there is an error in making the HTTP request.
    """
    response = requests.get(url)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")


def log_file_sensor_output(context):
    """
    Logs information about the file sensor task's execution context.

    Args:
        context (dict): The context dictionary containing task instance and execution details.
    """
    task_instance = context['task_instance']
    logger.info(f"Task {task_instance.task_id} has completed.")
    logger.info(f"Task state: {task_instance.state}")
    logger.info(f"Task start date: {task_instance.start_date}")
    logger.info(f"Task end date: {task_instance.end_date}")
    logger.info(f"Execution date: {task_instance.execution_date}")
    logger.info(f"Log URL: {task_instance.log_url}")


def final_task(output_path):
    """
    Reads the processed output file from Google Cloud Storage, cleans the data,
    and deletes rows with a salary less than 5000.0.

    Args:
        output_path (str): Path to the processed output file in GCS.

    Returns:
        None
    """
    # Extract bucket name and object name from the output path
    bucket_name = output_path.split("/")[0]  # Extract bucket name
    object_name = "/".join(output_path.split("/")[1:])

    gcs_hook = GCSHook()
    file_content = gcs_hook.download(
        bucket_name=bucket_name, object_name=object_name
    ).decode('utf-8')

    # Read the CSV content into a DataFrame
    df = pd.read_csv(io.StringIO(file_content))

    # Basic processing: correcting anomalous values
    df['Age'] = df['Age'].apply(lambda x: x if x > 0 else None)
    df['Salary'] = df['Salary'].apply(lambda x: x if x > 0 else None)
    df['City'] = df['City'].apply(lambda x: x if isinstance(x, str) else "Unknown")

    # Delete rows with salary less than 5000.0
    df = df[df['Salary'] >= 5000.0]

    # Print the cleaned data
    logger.info(f"Cleaned data: {df}")
