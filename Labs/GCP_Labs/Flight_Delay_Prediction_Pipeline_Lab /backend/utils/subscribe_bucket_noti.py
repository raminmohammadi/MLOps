from google.cloud import pubsub_v1
from google.oauth2 import service_account
import json
from dotenv import load_dotenv
import os
import signal

load_dotenv()

def create_subscriber():
    print("Running bucket subscriber...")
    credentials_dict = json.loads(os.environ.get('SERVICE_ACCOUNT_JSON'))
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path('mlops-final-lab', 'model-subscription')

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()
        
        data = json.loads(message.data.decode('utf-8'))
        object_name = data['name']
        
        if object_name.startswith("models/") and object_name.endswith("model.pkl"):
            print("Detected replacement of 'model.pkl' in the specified folder.")
            os.kill(os.getpid(), signal.SIGTERM)
    
    future = subscriber.subscribe(subscription_path, callback)

    try:
        future.result()
    except Exception as e:
        print(f"An error occurred: {e}")
        future.cancel()