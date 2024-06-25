from __future__ import annotations

from typing import Any

import os
import google.auth
from google.auth.transport.requests import AuthorizedSession
import requests
import functions_framework
import logging

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Following GCP best practices, these credentials should be
# constructed at start-up time and used throughout
# https://cloud.google.com/apis/docs/client-libraries-best-practices
AUTH_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
CREDENTIALS, _ = google.auth.default(scopes=[AUTH_SCOPE])


def make_composer2_web_server_request(
    url: str, method: str = "GET", **kwargs: Any
) -> google.auth.transport.Response:
    """
    Make a request to Cloud Composer 2 environment's web server.
    Args:
      url: The URL to fetch.
      method: The request method to use ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT',
        'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                  If no timeout is provided, it is set to 90 by default.
    """

    authed_session = AuthorizedSession(CREDENTIALS)

    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    return authed_session.request(method, url, **kwargs)


def trigger_dag(web_server_url: str, dag_id: str, data: dict) -> str:
    """
    Make a request to trigger a dag using the stable Airflow 2 REST API.
    https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

    Args:
      web_server_url: The URL of the Airflow 2 web server.
      dag_id: The DAG ID.
      data: Additional configuration parameters for the DAG run (json).
    """

    endpoint = f"api/v1/dags/{dag_id}/dagRuns"
    request_url = f"{web_server_url}/{endpoint}"
    json_data = {"conf": data}

    response = make_composer2_web_server_request(
        request_url, method="POST", json=json_data
    )

    if response.status_code == 403:
        raise requests.HTTPError(
            "You do not have permission to perform this operation. "
            "Check Airflow RBAC roles for your account."
            f"{response.headers} / {response.text}"
        )
    elif response.status_code != 200:
        response.raise_for_status()
    else:
        return response.text


@functions_framework.cloud_event
def trigger_dag_from_event(cloud_event):
    logger.info(f"Received cloud event: {cloud_event}")

    try:
        # Extract information from the cloud event
        event_data = cloud_event.data
        bucket_name = event_data['bucket']
        file_name = event_data['name']

        # Optional: Use these details to check if the uploaded file meets certain criteria
        logger.info(f"File {file_name} uploaded to {bucket_name} bucket.")

        # Set up parameters for triggering the Airflow DAG
        dag_id = os.getenv('DAG_ID').strip()
        execution_date = (
            None  # Set this to None if you want Airflow to use the current time
        )
        data = {"execution_date": execution_date}

        web_server_url = os.getenv('WEB_SERVER_URL').strip()

        # Trigger the DAG
        response = trigger_dag(web_server_url, dag_id, data)

        logger.info('DAG triggered successfully')
        logger.info(response)

    except Exception as e:
        logger.error(f"Error processing cloud event: {e}")
