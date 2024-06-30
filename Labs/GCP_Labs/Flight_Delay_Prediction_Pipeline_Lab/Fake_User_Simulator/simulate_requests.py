import pandas as pd
import requests
from tqdm import tqdm
import logging
import numpy as np
import sys
import os

# Configure logging
log_file_path = "simulation.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_file_path),
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

def send_batch(api_url, batch):
    for _, row in batch.iterrows():
        # Convert row to dictionary and replace NaN and infinite values
        payload = row.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict()
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                response_json = response.json()
                success = response_json.get('success', None)
                delayed = response_json.get('delayed', None)
                logger.info(f"Request successful: success={success}, delayed={delayed}")
            else:
                logger.error(f"Request failed: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            logger.error(f"Request error occurred: {e}")

def main(csv_file_path, api_url, batch_size=100):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Drop 'Unnamed: 27' column if it exists
    if 'Unnamed: 27' in df.columns:
        df.drop(columns=['Unnamed: 27'], inplace=True)
    
    for start in tqdm(range(0, len(df), batch_size), total=len(df) // batch_size):
        end = min(start + batch_size, len(df))
        batch = df.iloc[start:end]
        send_batch(api_url, batch)

if __name__ == "__main__":
    # Get the CSV file path and API URL from command-line arguments
    if len(sys.argv) != 3:
        logger.error("Usage: python simulate_requests.py <csv_file_path> <api_url>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    api_url = sys.argv[2]
    # Run the main function
    main(csv_file_path, api_url, batch_size=1000)