from google.cloud import storage
from google.oauth2 import service_account
import json
from dotenv import load_dotenv
import os

load_dotenv()

def download_blob(bucket_name, source_blob_name, destination_file_name):
    try:
        credentials_dict = json.loads(os.environ.get('SERVICE_ACCOUNT_JSON'))
        credentials = service_account.Credentials.from_service_account_info(credentials_dict)

        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)
        print(f"Downloaded storage object {source_blob_name} from bucket {bucket_name} to local file {destination_file_name}.")
    except Exception as e:
        print(e)
