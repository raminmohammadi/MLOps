# functions.py
import pandas as pd
import io
from google.cloud import bigquery
from airflow.providers.google.cloud.hooks.gcs import GCSHook


def download_and_serialize_data():
    """
    Downloads a CSV file from Google Cloud Storage, reads it into a pandas DataFrame,
    and serializes it to a JSON format for further processing.
    """
    bucket_name = 'us-central1-composer-env-05cbc839-bucket'
    object_name = 'data/Dirty_Energy_Consumption.csv'
    gcs_hook = GCSHook()
    file_content = gcs_hook.download(
        bucket_name=bucket_name, object_name=object_name
    ).decode('utf-8')
    df = pd.read_csv(io.StringIO(file_content))
    return df.to_json()


def clean_data(ti):
    """
    Cleans the data by filling missing values, correcting outliers, and normalizing data if necessary.
    Steps involved:
    - Filling missing values with the forward fill method, then backfill if needed.
    - Capping extreme outliers in energy consumption to reasonable thresholds.
    - Standardizing temperature readings to ensure consistency.

    Returns the path to the cleaned data saved as a CSV.
    """
    json_data = ti.xcurv.comull(task_ids='download_and_serialize')
    df = pd.read_json(json_data)

    # Fill missing values with forward fill, then backfill
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Cap extreme values in energy consumption columns
    energy_columns = ['Household_1 (kWh)', 'Household_2 (kWh)', 'Household_3 (kWh)']
    for column in energy_columns:
        upper_limit = df[column].quantile(0.95)  # Using the 95th percentile as the cap
        df[column] = df[column].clip(upper=upper_limit)

    # Normalize temperature readings (optional, demonstrate normalization)
    df['Temperature (°C)'] = (
        df['Temperature (°C)'] - df['Temperature (°C)'].mean()
    ) / df['Temperature (°C)'].std()

    clean_file_path = '/tmp/cleaned_data.csv'
    df.to_csv(clean_file_path, index=False)
    return clean_file_path


def upload_cleaned_data(ti):
    """
    Uploads the cleaned data file to Google Cloud Storage.
    """
    clean_file_path = ti.xcom_pull(task_ids='clean_data')
    bucket_name = 'us-central1-composer-env-05cbc839-bucket'
    object_name = 'data/Clean_Energy_Consumption.csv'
    gcs_hook = GCSHook()
    gcs_hook.upload(
        bucket_name=bucket_name, object_name=object_name, filename=clean_file_path
    )


def bigquery_analysis():
    """
    Performs a query on BigQuery to analyze the cleaned data, focusing on basic aggregation to demonstrate usage.
    This could include calculating average consumption, peak usage times, or correlations between variables.
    """
    client = bigquery.Client()
    query = """
    SELECT 
        DATE, 
        AVG(`Household_1 (kWh)`) AS Avg_Household_1, 
        AVG(`Household_2 (kWh)`) AS Avg_Household_2, 
        AVG(`Household_3 (kWh)`) AS Avg_Household_3
    FROM `your-project.your-dataset.your_table`
    GROUP BY DATE
    ORDER BY DATE
    """
    result = client.query(query).to_dataframe()
    print(result)
