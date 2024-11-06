# Advanced Google Cloud Composer and Airflow Project

Watch the tutorial video for this lab on our Youtube channel - [Tutorial Video](https://youtu.be/PKhUQBHpaAc)

## Overview

This project demonstrates advanced concepts in Google Cloud Composer and Airflow, including custom operators, integration with GCP services, monitoring and alerting, and security best practices. The project involves building a robust data pipeline that processes data, loads it into BigQuery, trains a machine learning model, and deploys the model to Google Cloud Storage (GCS).

## Key Concepts

### Custom Operators and Hooks

- **MLModelTrainOperator**: Custom operator to train a machine learning model using Keras and TensorFlow.
- **ModelDeployOperator**: Custom operator to deploy the trained model to GCS.

### Integration with Other GCP Services

- **Google Cloud Storage (GCS)**: Used for storing raw and processed data, as well as the trained machine learning model.
- **BigQuery**: Used for loading and analyzing processed data.
- **Google Cloud Monitoring and Logging**: Used for monitoring DAG execution, task performance, and system health.

### Advanced Monitoring and Alerting

- **Cloud Monitoring**: Set up to monitor DAG execution and task performance.
- **Cloud Logging**: Integrated to collect and view logs from Airflow tasks.
- **Stackdriver Alerting**: Configured to send alerts based on specific conditions or thresholds.

### Security and Access Control

- **IAM Policies**: Implemented to control access to Composer environments and GCP resources.
- **Encryption**: Ensured data security through encryption in transit and at rest.
- **Network Security**: Configured network policies to secure Composer environments.

## Project Structure

### DAG 1: Data Processing and BigQuery Integration

This DAG performs the following tasks:

1. **Download and Serialize Data**: Downloads raw data from a source and serializes it for processing.
2. **Clean Data**: Cleans the raw data to remove anomalies and missing values.
3. **Upload Cleaned Data**: Uploads the cleaned data to a GCS bucket.
4. **File Sensor**: Checks for the existence of the cleaned data file in GCS.
5. **Load to BigQuery**: Loads the cleaned data into a BigQuery table.
6. **BigQuery Analysis**: Performs analysis on the data in BigQuery.
7. **Send Email Notification**: Sends an email notification upon completion of the data processing tasks.
8. **Trigger Second DAG**: Triggers the second DAG for model training and deployment.

### DAG 2: Model Training and Deployment

This DAG performs the following tasks:

1. **Train Model**: Trains a machine learning model using the cleaned data from GCS.
2. **Deploy Model**: Deploys the trained model to GCS.

## Setup and Configuration

### Google Cloud Composer

1. **Create a Composer Environment**: Set up a Composer environment in Google Cloud.
2. **Install Required Packages**: Add necessary Python packages such as `keras`, `tensorflow`, and `google-cloud-storage`.
3. **Set Environment Variables**: Configure environment variables for email credentials and other sensitive information.

### IAM and Security

1. **Configure IAM Roles**: Ensure appropriate IAM roles and permissions are set for accessing GCS, BigQuery, and other GCP services.
2. **Network Policies**: Implement network policies to restrict access to the Composer environment.

### Monitoring and Logging

1. **Set Up Cloud Monitoring**: Configure Cloud Monitoring to track metrics and performance of your Airflow tasks.
2. **Set Up Cloud Logging**: Enable Cloud Logging to collect logs from your Airflow tasks.
3. **Configure Stackdriver Alerts**: Set up alerts based on specific conditions or thresholds in Stackdriver.

## Running the Project

1. **Deploy DAGs**: Upload the DAG files (`dag_tasks.py` and `model_training_and_deployment.py`) to your Composer environment.
2. **Trigger DAGs**: Manually trigger the first DAG from the Airflow UI or set it to run on a schedule.
3. **Monitor Execution**: Use Cloud Monitoring and Logging to monitor the execution of your DAGs and tasks.

## Conclusion

This project demonstrates the integration of advanced features and best practices in Google Cloud Composer and Airflow. By leveraging custom operators, GCP services, and robust monitoring and security configurations, we have built a scalable and secure data processing pipeline.

## References

- [Google Cloud Composer Documentation](https://cloud.google.com/composer/docs)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Google Cloud Monitoring](https://cloud.google.com/monitoring)
- [Google Cloud Logging](https://cloud.google.com/logging)
- [TensorFlow and Keras Documentation](https://www.tensorflow.org/)

