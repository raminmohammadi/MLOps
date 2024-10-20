# Cloud Run on GCP

This guide will walk you through deploying a containerized application on Google Cloud Run and using Google Cloud Storage buckets to store files. 

## Prerequisites

- A Google Cloud Platform (GCP) account
- Google Cloud SDK installed on your local machine
- A GCP project created
- Docker installed locally

## Step 1: Enable APIs

1. **Enable Cloud Run and Cloud Storage APIs**  
   First, ensure that the Cloud Run and Cloud Storage APIs are enabled for your project. You can enable them from the Cloud Console or by running the following command:
   
   ```bash
   gcloud services enable run.googleapis.com storage.googleapis.com
   ```

## Step 2: Set up a Google Cloud Storage Bucket

1. **Create a bucket**  
   Navigate to the [Cloud Storage Console](https://console.cloud.google.com/storage) and create a new bucket. Make sure to choose a globally unique name.

   Or use the following command to create a bucket:
   
   ```bash
   gsutil mb -l [REGION] gs://[BUCKET_NAME]/
   ```

2. **Upload files to the bucket (optional)**  
   You can upload files to your bucket using the Cloud Console or the `gsutil` command:
   
   ```bash
   gsutil cp [FILE_PATH] gs://[BUCKET_NAME]/
   ```

## Step 3: Write a Basic Python Flask App

1. **Create a simple `app.py` file**  
   Write a simple Flask app that interacts with the bucket.

   ```python
   from flask import Flask, jsonify
   from google.cloud import storage

   app = Flask(__name__)

   @app.route('/')
   def list_files():
       """List files in Google Cloud Storage bucket."""
       storage_client = storage.Client()
       bucket = storage_client.get_bucket('your-bucket-name')
       blobs = bucket.list_blobs()

       files = [blob.name for blob in blobs]
       return jsonify(files)

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
   ```

2. **Install dependencies**  
   Create a `requirements.txt` file:

   ```txt
   Flask==2.0.1
   google-cloud-storage==1.42.0
   ```

## Step 4: Dockerize the Application

1. **Create a Dockerfile**  
   Create a `Dockerfile` for your Flask app:

   ```Dockerfile
   # Use the official Python image from the Docker Hub
   FROM python:3.9-slim

   # Set the working directory
   WORKDIR /app

   # Copy the current directory contents into the container at /app
   COPY . /app

   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt

   # Make port 8080 available to the world outside this container
   EXPOSE 8080

   # Run app.py when the container launches
   CMD ["python", "app.py"]
   ```

2. **Build the Docker image**  
   Build your Docker image locally:

   ```bash
   docker build -t gcr.io/[PROJECT-ID]/flask-cloud-run:latest .
   ```

## Step 5: Push the Docker Image to Google Container Registry (GCR)

1. **Authenticate Docker with GCR**  
   Authenticate Docker to Google Cloud:

   ```bash
   gcloud auth configure-docker
   ```

2. **Push the image to GCR**  
   Push your Docker image to Google Container Registry:

   ```bash
   docker push gcr.io/[PROJECT-ID]/flask-cloud-run:latest
   ```

## Step 6: Deploy to Google Cloud Run

1. **Deploy your service to Cloud Run**  
   Deploy your containerized app to Cloud Run using the following command:

   ```bash
   gcloud run deploy flask-cloud-run \
   --image gcr.io/[PROJECT-ID]/flask-cloud-run:latest \
   --platform managed \
   --region [REGION] \
   --allow-unauthenticated
   ```

2. **Note the service URL**  
   After deployment, note the URL provided by Cloud Run where your application is live.

## Step 7: Test the Application

Visit the Cloud Run service URL to confirm that your application is running and listing the files in the specified Cloud Storage bucket.

## Step 8: Clean Up (Optional)

To avoid incurring charges, delete the resources you created:

1. **Delete the Cloud Run service**  
   ```bash
   gcloud run services delete flask-cloud-run
   ```

2. **Delete the GCS bucket**  
   ```bash
   gsutil rm -r gs://[BUCKET_NAME]
   ```

3. **Delete the Docker image from GCR**  
   ```bash
   gcloud container images delete gcr.io/[PROJECT-ID]/flask-cloud-run:latest
   ```

---

This README provides a straightforward guide for deploying a Python Flask app with Google Cloud Run and interacting with Google Cloud Storage buckets. Be sure to replace placeholders like `[PROJECT-ID]`, `[BUCKET_NAME]`, and `[REGION]` with your actual project values.


