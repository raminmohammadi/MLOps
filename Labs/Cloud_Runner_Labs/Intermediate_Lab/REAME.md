# Cloud Run Intermediate Lab

Welcome to the intermediate lab on **Google Cloud Run**! In this lab, you will build upon the basic lab by deploying a more complex containerized application that interacts with **Google Cloud Storage** and **BigQuery**. You will learn how to use environment variables, set up authentication for accessing other Google Cloud services, and monitor application logs.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Set Up Google Cloud Project and Resources](#step-1-set-up-google-cloud-project-and-resources)
- [Step 2: Create and Containerize the Application](#step-2-create-and-containerize-the-application)
- [Step 3: Push the Docker Image to Container Registry](#step-3-push-the-docker-image-to-container-registry)
- [Step 4: Deploy to Google Cloud Run](#step-4-deploy-to-google-cloud-run)
- [Step 5: Access and Test the Application](#step-5-access-and-test-the-application)
- [Step 6: Monitor and Log the Service](#step-6-monitor-and-log-the-service)
- [Step 7: Clean Up Resources](#step-7-clean-up-resources)
- [Conclusion](#conclusion)

---

## Prerequisites

- **Google Cloud Account**: Make sure you have a Google Cloud account with billing enabled.
- **Google Cloud SDK**: Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) on your local machine.
- **Docker**: Ensure Docker is installed and running on your machine.
- **Basic Knowledge**: Familiarity with Python, Flask, and Docker.

---

## Step 1: Set Up Google Cloud Project and Resources

### 1. Create a Google Cloud Project

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Click on the project dropdown and select **New Project**.
- Enter a **Project Name** (e.g., `cloud-run-intermediate-lab`).
- Click **Create**.
- Note the **Project ID**; you will need it later.

### 2. Enable Necessary APIs

- Navigate to **APIs & Services > Library**.
- Enable the following APIs:
  - **Cloud Run API**
  - **Cloud Storage API**
  - **BigQuery API**

### 3. Create a Google Cloud Storage Bucket

- Go to **Navigation Menu > Cloud Storage > Buckets**.
- Click **Create bucket**.
- Enter a **Name** for your bucket (must be globally unique, e.g., `cloud-run-intermediate-lab-bucket`).
- Choose a **Location Type** and **Region** (e.g., **Region** and `us-central1`).
- Select a **Storage Class** (e.g., **Standard**).
- Click **Create**.

### 4. Set Up a Service Account

- Navigate to **IAM & Admin > Service Accounts**.
- Click **Create Service Account**.
- Enter a **Service Account Name** (e.g., `cloud-run-service-account`).
- Click **Create and Continue**.
- Assign the following roles:
  - **Storage Admin**
  - **BigQuery User**
- Click **Done**.
- Note the **Service Account Email** for later use.

---

## Step 2: Create and Containerize the Application

### 1. Create the Application Directory

```bash
mkdir cloud-run-intermediate-app
cd cloud-run-intermediate-app
```

### 2. Write the Python Application

Create a file named `app.py` with the following content:

```python
from flask import Flask
from google.cloud import storage, bigquery
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello from the intermediate lab!"

@app.route('/upload')
def upload_file():
    # Initialize Cloud Storage client
    storage_client = storage.Client()
    bucket_name = os.environ.get('BUCKET_NAME')
    if not bucket_name:
        return 'BUCKET_NAME environment variable is not set.', 500
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('hello.txt')
    blob.upload_from_string('Hello, Cloud Storage!')
    return f'File uploaded to {bucket_name}.'

@app.route('/query')
def query_bigquery():
    # Initialize BigQuery client
    client = bigquery.Client()
    query = """
        SELECT name, SUM(number) as total
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = 'TX'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 10
    """
    query_job = client.query(query)
    results = query_job.result()
    names = [row.name for row in results]
    return f'Top names in Texas: {", ".join(names)}'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

### 3. Create a Requirements File

Create a file named `requirements.txt`:

```
Flask==2.0.1
google-cloud-storage==1.42.3
google-cloud-bigquery==2.24.0
```

### 4. Create a Dockerfile

Create a file named `Dockerfile`:

```Dockerfile
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 for serving the app
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]
```

### 5. Build the Docker Image

Replace `YOUR_PROJECT_ID` with your actual project ID.

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/cloud-run-intermediate-app .
```

---

## Step 3: Push the Docker Image to Container Registry

### 1. Authenticate Docker with Google Cloud

```bash
gcloud auth configure-docker
```

### 2. Push the Image

```bash
docker push gcr.io/YOUR_PROJECT_ID/cloud-run-intermediate-app
```

---

## Step 4: Deploy to Google Cloud Run

### 1. Deploy Using gcloud Command

Replace the placeholders with your actual values.

```bash
gcloud run deploy cloud-run-intermediate-service \
  --image gcr.io/YOUR_PROJECT_ID/cloud-run-intermediate-app \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --update-env-vars BUCKET_NAME=YOUR_BUCKET_NAME \
  --service-account YOUR_SERVICE_ACCOUNT_EMAIL
```

- **YOUR_PROJECT_ID**: Your Google Cloud project ID.
- **YOUR_BUCKET_NAME**: The name of your Cloud Storage bucket.
- **YOUR_SERVICE_ACCOUNT_EMAIL**: The email of the service account created earlier.

### 2. Grant the Service Account Access

Ensure the service account has the necessary permissions.

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL \
  --role=roles/storage.admin

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL \
  --role=roles/bigquery.user
```

---

## Step 5: Access and Test the Application

### 1. Get the Service URL

After deployment, note the service URL output in the terminal or retrieve it:

```bash
gcloud run services describe cloud-run-intermediate-service \
  --platform managed \
  --region us-central1 \
  --format "value(status.url)"
```

### 2. Test the Endpoints

#### Test the Root Endpoint

```bash
curl https://YOUR_SERVICE_URL/
```

You should see:

```
Hello from the intermediate lab!
```

#### Test the Upload Endpoint

```bash
curl https://YOUR_SERVICE_URL/upload
```

Verify that `hello.txt` has been uploaded to your Cloud Storage bucket.

#### Test the BigQuery Endpoint

```bash
curl https://YOUR_SERVICE_URL/query
```

You should receive a list of top names in Texas.

---

## Step 6: Monitor and Log the Service

### 1. View Logs in Cloud Console

- Navigate to **Cloud Run** in the Google Cloud Console.
- Click on your service **cloud-run-intermediate-service**.
- Go to the **Logs** tab to view application logs.

### 2. Monitor Metrics

- In the Cloud Run service details, navigate to the **Metrics** tab.
- Observe metrics like CPU usage, memory usage, and request latency.

---

## Step 7: Clean Up Resources

To avoid incurring charges, clean up the resources you created.

### 1. Delete the Cloud Run Service

```bash
gcloud run services delete cloud-run-intermediate-service --region us-central1
```

### 2. Delete the Container Image

```bash
gcloud container images delete gcr.io/YOUR_PROJECT_ID/cloud-run-intermediate-app --force-delete-tags
```

### 3. Delete the Cloud Storage Bucket

```bash
gsutil rm -r gs://YOUR_BUCKET_NAME
```

### 4. Delete the Service Account (Optional)

If you no longer need the service account:

```bash
gcloud iam service-accounts delete YOUR_SERVICE_ACCOUNT_EMAIL
```

---

## Conclusion

Congratulations on completing the **Cloud Run Intermediate Lab**!

In this lab, you:

- **Set up** a Google Cloud project with Cloud Run, Cloud Storage, and BigQuery.
- **Created** a Flask application that interacts with Cloud Storage and BigQuery.
- **Containerized** the application using Docker.
- **Deployed** the application to Cloud Run with environment variables and a service account.
- **Tested** the application endpoints to ensure functionality.
- **Monitored** logs and metrics through the Cloud Console.
- **Cleaned up** resources to prevent unwanted charges.

This lab has provided you with a deeper understanding of deploying complex applications on Google Cloud Run and integrating other Google Cloud services.

---
