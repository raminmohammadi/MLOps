import pandas as pd
import numpy as np
import warnings
import logging
import calendar
from google.cloud import storage

warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    try:
        # Data Loading
        logging.info("Loading data from GCS")

        # Initialize a client
        storage_client = storage.Client()

        # Define the bucket name
        bucket_name = 'us-central1-mlops-composer-c43be234-bucket'
        data_prefix = 'data/'  # This is the folder within the bucket where your CSV files are stored

        # Get the bucket
        bucket = storage_client.bucket(bucket_name)

        # List all blobs in the specified folder
        blobs = bucket.list_blobs(prefix=data_prefix)

        # Initialize an empty list to store DataFrames
        dfs = []

        # Iterate over the blobs and read each CSV file
        for blob in blobs:
            if blob.name.endswith('.csv'):
                logging.info(f"Loading data from {blob.name}")
                blob_path = f'gs://{bucket_name}/{blob.name}'
                df = pd.read_csv(blob_path)
                dfs.append(df)

        # Combine all DataFrames
        df = pd.concat(dfs, ignore_index=True)
        logging.info("Data combined successfully")

        # Renaming Airlines
        logging.info("Renaming airlines")
        df['OP_CARRIER'].replace(
            {
                'UA': 'United Airlines',
                'AS': 'Alaska Airlines',
                '9E': 'Endeavor Air',
                'B6': 'JetBlue Airways',
                'EV': 'ExpressJet',
                'F9': 'Frontier Airlines',
                'G4': 'Allegiant Air',
                'HA': 'Hawaiian Airlines',
                'MQ': 'Envoy Air',
                'NK': 'Spirit Airlines',
                'OH': 'PSA Airlines',
                'OO': 'SkyWest Airlines',
                'VX': 'Virgin America',
                'WN': 'Southwest Airlines',
                'YV': 'Mesa Airline',
                'YX': 'Republic Airways',
                'AA': 'American Airlines',
                'DL': 'Delta Airlines',
            },
            inplace=True,
        )

        # Dropping Columns
        logging.info("Dropping unnecessary columns")
        df = df.drop(["Unnamed: 27"], axis=1)

        # Handling Cancelled Flights
        logging.info("Handling cancelled flights")
        df = df[df['CANCELLED'] == 0]
        df = df.drop(['CANCELLED'], axis=1)

        # Handling Cancellation Codes
        logging.info("Dropping cancellation codes")
        df = df.drop(["CANCELLATION_CODE"], axis=1)

        # Dropping DIVERTED column
        logging.info("Dropping diverted column")
        df = df.drop(['DIVERTED'], axis=1)

        # Dropping Delay Reason Columns
        logging.info("Dropping delay reason columns")
        df = df.drop(
            [
                'CARRIER_DELAY',
                'WEATHER_DELAY',
                'NAS_DELAY',
                'SECURITY_DELAY',
                'LATE_AIRCRAFT_DELAY',
            ],
            axis=1,
        )

        # Dropping Flight Number
        logging.info("Dropping flight number")
        df = df.drop(['OP_CARRIER_FL_NUM'], axis=1)

        # Dropping Time Columns
        logging.info("Dropping time columns")
        df.drop(columns=['DEP_TIME', 'ARR_TIME'], inplace=True)

        # Handling Missing Values
        logging.info("Handling missing values")
        df["DEP_DELAY"] = df["DEP_DELAY"].fillna(0)
        df['TAXI_IN'].fillna((df['TAXI_IN'].mean()), inplace=True)
        df = df.dropna()

        # Binning Time Columns
        logging.info("Binning time columns")
        time_columns = ['CRS_DEP_TIME', 'WHEELS_OFF', 'WHEELS_ON', 'CRS_ARR_TIME']
        for col in time_columns:
            df[col] = np.ceil(df[col] / 600).astype(int)

        # Extracting Date Information
        logging.info("Extracting date information")
        df['DAY'] = pd.DatetimeIndex(df['FL_DATE']).day
        df['MONTH'] = pd.DatetimeIndex(df['FL_DATE']).month

        df['MONTH_AB'] = df['MONTH'].apply(lambda x: calendar.month_abbr[x])

        # Binary Classification
        logging.info("Applying binary classification")
        df['FLIGHT_STATUS'] = df['ARR_DELAY'].apply(lambda x: 0 if x < 0 else 1)

        # Convert FL_DATE to datetime and extract weekday
        logging.info("Converting FL_DATE to datetime and extracting weekday")
        df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
        df['WEEKDAY'] = df['FL_DATE'].dt.dayofweek

        # Drop unnecessary columns
        logging.info("Dropping unnecessary columns")
        df = df.drop(columns=['FL_DATE', 'MONTH_AB', 'ARR_DELAY'])

        # Saving the Cleaned Data
        logging.info("Saving cleaned data to cleaned.csv")
        df.to_csv('cleaned.csv', index=False)
        logging.info("Cleaned data saved successfully")

    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
