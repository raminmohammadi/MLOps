import functions_framework
import os
import googleapiclient.discovery
from google.auth import compute_engine
import re

@functions_framework.cloud_event
def start_vm(event):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    # Access the event data
    data = event.data

    # Print the event details for debugging purposes
    print(f"Processing file: {data['name']} from bucket: {data['bucket']}.")

    # Load environment variables
    PROJECT_ID = os.getenv('PROJECT_ID')
    ZONE = os.getenv('ZONE')
    INSTANCE_NAME_PREFIX = os.getenv('INSTANCE_NAME_PREFIX')
    CUSTOM_IMAGE = os.getenv('CUSTOM_IMAGE')
    API_URL = os.getenv('API_URL')

    # Check if any variable is missing
    if not all([PROJECT_ID, ZONE, INSTANCE_NAME_PREFIX, CUSTOM_IMAGE, API_URL]):
        raise ValueError("Missing one or more environment variables: PROJECT_ID, ZONE, INSTANCE_NAME_PREFIX, CUSTOM_IMAGE, API_URL")

    credentials = compute_engine.Credentials()
    compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    # Get the file name and bucket from the event
    file_name = data['name']
    bucket_name = data['bucket']

    # Sanitize the instance name to conform to the required format
    instance_id = re.sub(r'[^-a-z0-9]', '-', file_name.split('.')[0].lower())[:60]
    instance_name = f"{INSTANCE_NAME_PREFIX}-{instance_id}"

    # Ensure the CUSTOM_IMAGE is a full URL
    if not CUSTOM_IMAGE.startswith('projects/'):
        raise ValueError("CUSTOM_IMAGE must be a full URL in the format 'projects/IMAGE_PROJECT/global/images/IMAGE'")

    # Configure the instance properties
    instance_body = {
        'name': instance_name,
        'machineType': f"zones/{ZONE}/machineTypes/n1-standard-1",
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': CUSTOM_IMAGE
                }
            }
        ],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        'metadata': {
            'items': [
                {
                    'key': 'startup-script',
                    'value': f"""
                        #! /bin/bash
                        # Copy the uploaded file from Cloud Storage to the VM
                        gsutil cp gs://{bucket_name}/{file_name} /home/user_simulator/{file_name}
                        # Set up and activate the virtual environment
                        cd /home/user_simulator
                        . venv/bin/activate
                        # Run the Python script with arguments
                        python3 simulate_requests.py /home/user_simulator/{file_name} {API_URL}
                        # Schedule instance shutdown after script completion
                        sudo shutdown -h now
                    """
                },
                {
                    'key': 'shutdown-script',
                    'value': f"""
                        #! /bin/bash
                        gcloud compute instances delete {instance_name} --zone={ZONE} --quiet
                    """
                }
            ]
        },
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        }]
    }
    request = compute.instances().insert(
        project=PROJECT_ID,
        zone=ZONE,
        body=instance_body
    )
    response = request.execute()
    print(response)