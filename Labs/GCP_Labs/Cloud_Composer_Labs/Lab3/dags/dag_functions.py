# functions.py
import pandas as pd
import io
from google.cloud import bigquery, aiplatform
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.models import Variable
import smtplib
from email.mime.text import MIMEText
import logging

AIRFLOW_TASK = "airflow.task"
logger = logging.getLogger(AIRFLOW_TASK)


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
    json_data = ti.xcom_pull(task_ids='download_and_serialize')
    df = pd.read_json(json_data)

    # Fill missing values with forward fill, then backfill
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # Cap extreme values in energy consumption columns
    energy_columns = ['Household_1', 'Household_2', 'Household_3']
    for column in energy_columns:
        upper_limit = df[column].quantile(0.95)  # Using the 95th percentile as the cap
        df[column] = df[column].clip(upper=upper_limit)

    # Normalize temperature readings (optional, demonstrate normalization)
    df['Temperature'] = (df['Temperature'] - df['Temperature'].mean()) / df[
        'Temperature'
    ].std()

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
        AVG(`Household_1`) AS Avg_Household_1, 
        AVG(`Household_2`) AS Avg_Household_2, 
        AVG(`Household_3`) AS Avg_Household_3
    FROM `usecentraldataset.my_new_table`
    -- Last 30 days filter
    GROUP BY DATE
    ORDER BY DATE
    """
    result = client.query(query).to_dataframe()
    logger.info(f"Output of the bigquery analysis is{result}")


def send_email():
    sender_email = Variable.get('EMAIL_USER')
    receiver_email = "{your_email}"
    password = Variable.get('EMAIL_PASSWORD')

    subject = "Sample email from Airflow"
    body = "Hello, this is a test email from Python."

    # Create the email headers and content
    email_message = MIMEText(body)
    email_message['Subject'] = subject
    email_message['From'] = sender_email
    email_message['To'] = receiver_email

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email_message.as_string())
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
    finally:
        server.quit()


def fetch_and_predict(**context):
    project_id = context['params']['project_id']
    endpoint_id = context['params']['endpoint_id']
    instances = context['params']['instances']

    aiplatform.init(project=project_id)

    endpoint = aiplatform.Endpoint(endpoint_id)

    response = endpoint.predict(instances=instances)
    predictions = response.predictions

    print(f'Predictions: {predictions}')
