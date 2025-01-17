import os
import re
from google.cloud import container_v1
from google.protobuf.json_format import MessageToDict
import functions_framework

@functions_framework.cloud_event
def start_gke_on_file_upload(cloud_event):
    """Triggered by a finalized Cloud Storage event."""
    try:
        # Parse Cloud Event data
        data = cloud_event.data
        bucket = data.get("bucket")
        file_name = data.get("name")
        print(f"DEBUG: File uploaded to bucket: {bucket}, name: {file_name}")

        # Generate a valid cluster name
        sanitized_name = re.sub(r"[^a-z0-9-]", "-", file_name.lower()).strip("-")
        cluster_name = sanitized_name[:40]  # Ensure the name is no longer than 40 characters
        print(f"DEBUG: Sanitized cluster name: {cluster_name}")

        # Fetch environment variables
        project_id = os.getenv("PROJECT_ID")
        zone = os.getenv("ZONE")
        print(f"DEBUG: PROJECT_ID={project_id}, ZONE={zone}")

        # Validate environment variables
        if not project_id or not zone:
            raise ValueError("Environment variables PROJECT_ID and ZONE are required.")

        # Initialize GKE client
        client = container_v1.ClusterManagerClient()

        # Define cluster configuration
        cluster_config = {
            "name": cluster_name,
            "initial_node_count": 3,
            "node_config": {
                "machine_type": "e2-medium",
                "disk_size_gb": 100,
            },
        }

        # Start cluster creation
        response = client.create_cluster(
            project_id=project_id,
            zone=zone,
            cluster=cluster_config,
        )
        print("DEBUG: Cluster creation response:", response)

        # Log success
        response_dict = MessageToDict(response)
        print(f"Cluster creation initiated successfully: {response_dict}")

    except Exception as e:
        print(f"ERROR: {e}")
