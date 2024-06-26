# Flight Delay Prediction Model Pipeline

## Table of Contents
1. [Overview](#overview)
2. [Dataset](#dataset)
3. [Data Processing and Model Training Pipeline](#data-processing-and-model-training-pipeline)
   1. [Data Storage](#data-storage)
   2. [Dockerization and Deployment](#dockerization-and-deployment)
   3. [Triggering the DAG](#triggering-the-dag)
   4. [Google Batch Job Execution](#google-batch-job-execution)
   5. [Model and Preprocessor Upload](#model-and-preprocessor-upload)
4. [Model Deployment with FastAPI on GKE](#model-deployment-with-FastAPI-on-gke)
   1. [Deployment using Google Kubernetes Engine (GKE)](#deployment-using-google-kubernetes-engine-gke)
   2. [Model Update Mechanism](#model-update-mechanism)
5. [Simulation Service for Load Testing](#simulation-service-for-load-testing)
6. [CI/CD Pipeline Using GitHub Actions](#cicd-pipeline-using-github-actions)
   1. [Deploy FastAPI Service to Kubernetes](#1-deploy-FastAPI-service-to-kubernetes)
   2. [Upload DAGs to GCS](#2-upload-dags-to-gcs)
   3. [Build and Push Docker Image for Preprocessing and Model Training](#3-build-and-push-docker-image-for-preprocessing-and-model-training)

## Overview

This project implements a machine learning workflow for predicting flight delays. The workflow includes data preprocessing, model training, and model deployment, all orchestrated using Google Cloud Composer and executed via Google Batch jobs. The trained model is deployed using a FastAPI server for predictions.

## Dataset

- **Source:** "Airline Delay and Cancellation Data, 2009 - 2018" from Kaggle 
https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018
- **Description:** Extensive timeseries data on flight delays and cancellations
- **Processing:** Split into manageable 4-month chunks for easier processing and analysis
- **Storage:** Hosted securely in Google Cloud Storage (GCS) buckets

## Data Processing and Model Training Pipeline

### Data Storage

**Training Data Storage:** 

- **GCS Buckets:** Training data files are stored in Google Cloud Storage (GCS) buckets. This setup ensures scalable and reliable data access.

### Dockerization and Deployment

**Implementation Details:**

- **Containerization:** The preprocessing and model training code are containerized to ensure consistency across different environments.
- **Deployment to GCR:** The Docker image is pushed to Google Container Registry (GCR) for efficient storage and retrieval.

**Steps:**
1. **Dockerization:**
   - A Dockerfile defines the environment and dependencies required for data preprocessing and model training.
   - Github Actions is used to build an image from the Dockerfile and push it to GCR.

2. **Deployment to GCR:**
   - GitHub Actions automate the building and pushing of the Docker image to GCR.
   - Authentication to GCP is handled within the GitHub Actions workflow.
   - The Docker image is built and pushed to GCR.

### Triggering the DAG

**Implementation Details:**

- **Automate Initiation:** A Cloud Function triggers the data processing and model training pipeline when new data is uploaded to GCS.

**Steps:**
1. **Trigger on Data Upload:**
   - A Cloud Function is triggered by the Google Cloud Storage whenever new data is detected on the mentioned trigger bucket.

2. **Initiate DAG:**
   - The Cloud Function initiates a Directed Acyclic Graph (DAG) in Cloud Composer (Airflow).
   - The DAG orchestrates the subsequent steps in the pipeline.

### Google Batch Job Execution

**Implementation Details:**

- **Execute Preprocessing and Training:** Google Batch is used to run data preprocessing and model training tasks.

**Steps:**
1. **Setup Batch Job:**
   - The DAG sets up a Google Batch job using the Docker image from GCR.
   - The job configuration is defined, including the commands to execute within the Docker container.

2. **Execute Commands:**
   - The batch job performs data preprocessing and model training.
   - The job is monitored for completion or errors by GCSObjectExistenceSensor. This checks if the model pickle file is uploaded to GCS.

3. **Delete the Batch Job**
   - Upon successful completion of the batch job, a subsequent task in the DAG will automatically delete the batch job setup, optimizing both cost and compute usage.

### Model and Preprocessor Upload

**Implementation Details:**

- **Store Outputs:** The preprocessed data and trained model are uploaded to GCS for future use.

**Steps:**
1. **Upload to GCS:**
   - After the batch job completes, the preprocessed data and trained model (saved as a pickle file) are uploaded to the GCS bucket.

## Model Deployment with FastAPI on GKE

### Deployment using Google Kubernetes Engine (GKE)

**Implementation Details:**

- **Deploy APIs:** Scalable APIs are deployed on GKE to serve predictions based on trained models.

**Steps:**
1. **Configure GKE Cluster:**
   - A GKE cluster with auto-scaling capabilities is set up to handle varying loads.

2. **Deploy FastAPI:**
   - The FastAPI application is containerized.
   - The FastAPI containers are deployed to GKE nodes.

### Model Update Mechanism

**Implementation Details:**

- **Update Model Automatically:** The model is retrained with new data and the FastAPI application is updated with the new model.

**Steps:**
1. **Trigger on New Data Upload:**
   - When new data is uploaded to the GCS bucket, it triggers the DAG in Cloud Composer to retrain the model.

2. **Retrain Model:**
   - The retraining process is executed in the DAG using the new data.

3. **Upload Updated Model to GCS:**
   - After retraining, the updated model is uploaded to the GCS bucket.

4. **Update FastAPI Service:**
   - The FastAPI service subscribes to a Pub/Sub topic.
   - The updated model is fetched from GCS and the model used for predictions is updated.

## Simulation Service for Load Testing

### Fake User Simulation Service

**Implementation Details:**

- **Test Service Scalability:** Simulate load on the flight delay prediction service to trigger autoscaling.

**Steps:**
1. **Create VM Instance:**
   - A VM instance in Google Cloud is set up to run the simulation.

2. **Install Software:**
   - Necessary software is installed and the load simulation script is uploaded to the VM.

3. **Create Custom Image:**
   - A custom VM image is created from the configured instance for consistency.

4. **Automate VM Creation:**
   - A Cloud Function automates VM creation and script execution when new data is uploaded.

5. **Monitor Autoscaling:**
   - The GKE cluster is observed to ensure it scales in response to the simulated load.

## CI/CD Pipeline Using GitHub Actions

### 1. Deploy FastAPI Service to Kubernetes

**Implementation Details:**

- **Automate Deployment:** The deployment of the FastAPI service to GKE is streamlined using GitHub Actions.

**Pipeline Steps:**
1. **Checkout Code:** The latest code is fetched.
2. **Authenticate to GCP:** A Google Cloud service account key is used to authenticate.
3. **Build Docker Image:** The Docker image for the FastAPI service is built.
4. **Push to GCR:** The Docker image is pushed to Google Container Registry.
5. **Deploy to GKE:** The Kubernetes configurations are applied to deploy the FastAPI service to GKE.

### 2. Upload DAGs to GCS

**Implementation Details:**

- **Automate DAG Deployment:** DAGs are automatically uploaded to Google Cloud Storage using GitHub Actions.

**Pipeline Steps:**
1. **Checkout Code:** The latest code is fetched.
2. **Set up Python Environment:** The required Python version is installed.
3. **Install GCloud SDK:** The Google Cloud SDK is installed.
4. **Authenticate to GCP:** A Google Cloud service account key is used to authenticate.
5. **Upload DAGs to GCS:** `gsutil` is used to sync the DAGs directory with the specified GCS bucket.

### 3. Build and Push Docker Image for Preprocessing and Model Training

**Implementation Details:**

- **Automate the Build and Push:** The building and pushing of Docker images for preprocessing and model training are streamlined.

**Pipeline Steps:**
1. **Checkout Code:** The latest code is fetched.
2. **Install GCloud CLI:** The Google Cloud CLI is installed.
3. **Authenticate to GCP:** A Google Cloud service account key is used to authenticate.
4. **Build Docker Image:** The Docker image for preprocessing and model training is built.
5. **Push to GCR:** The Docker image is pushed to Google Container Registry.

---

By following this guide, you can set up a robust machine learning workflow on Google Cloud Platform, leveraging Cloud Composer, Google Batch, and Google Cloud Storage for end-to-end model training and deployment.