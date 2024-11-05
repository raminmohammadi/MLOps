import json
import pandas as pd
from google.cloud import pubsub_v1
from google.cloud import storage

# Initialize Publisher client and topic path
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('PROJECT_ID', 'model-training-trigger') # Replace with Project_ID


storage_client = storage.Client()

def process_data(event, context):
    """Triggered by Cloud Storage when new data is uploaded."""
    file_data = event
    bucket_name = file_data['bucket']
    file_name = file_data['name']

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    file_contents = blob.download_as_text()

    from io import StringIO
    data = pd.read_csv(StringIO(file_contents))

    stats = data.describe().to_dict()

    processed_data = {
        "status": "data_processed",
        "file": file_name,
        "stats": stats
    }

    # Publish message to Pub/Sub
    publisher.publish(topic_path, json.dumps(processed_data).encode('utf-8'))

    print(f"Data from {file_name} processed and message published to {topic_path}")
    print(f"Data Stats: {stats}")
    return f'Data processed and message published for file {file_name}'
