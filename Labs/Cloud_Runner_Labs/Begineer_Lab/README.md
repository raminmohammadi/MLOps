# Cloud Runner Basic Lab

This guide will help you create a very basic lab using Cloud Runner and Google Cloud Platform (GCP) buckets. You can use this step-by-step guide to set up a simple lab environment and upload it as a README to your GitHub repository.

## Prerequisites

- A Google Cloud account with necessary permissions.
- Cloud SDK installed and set up on your local machine.
- Basic understanding of command line usage.

## Steps to Create a Basic Cloud Runner Lab

### Step 1: Set Up Google Cloud Project
1. **Create a new GCP project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown in the top left and select "New Project."
   - Give your project a name and click "Create."
2. **Set the active project**:
   - Open a terminal and set your active GCP project with the command:
   ```bash
   gcloud config set project <YOUR_PROJECT_ID>
   ```

### Step 2: Create a Cloud Storage Bucket
1. **Create a new bucket**:
   - Use the Cloud Console or run the following command to create a bucket:
   ```bash
   gsutil mb gs://<YOUR_BUCKET_NAME>
   ```
   Replace `<YOUR_BUCKET_NAME>` with a unique name for your bucket.
2. **Verify the bucket**:
   - Run the command to list all buckets:
   ```bash
   gsutil ls
   ```
   - You should see your newly created bucket listed.

### Step 3: Upload a File to the Bucket
1. **Create a sample file**:
   - Create a text file to upload:
   ```bash
   echo "Hello, Cloud Runner!" > sample.txt
   ```
2. **Upload the file to the bucket**:
   - Use the `gsutil cp` command to upload:
   ```bash
   gsutil cp sample.txt gs://<YOUR_BUCKET_NAME>/
   ```
3. **Verify the upload**:
   - List the files in your bucket:
   ```bash
   gsutil ls gs://<YOUR_BUCKET_NAME>/
   ```

### Step 4: Set Up Cloud Runner
1. **Install Cloud Runner**:
   - If not already installed, follow the [Cloud Runner installation guide](https://example.com/cloud-runner-install) to install it on your machine.
2. **Authenticate Cloud Runner**:
   - Authenticate Cloud Runner to access your GCP resources:
   ```bash
   cloud-runner auth login --project <YOUR_PROJECT_ID>
   ```

### Step 5: Execute a Cloud Runner Job
1. **Create a Cloud Runner script**:
   - Create a file called `runner_script.sh` with the following content:
   ```bash
   #!/bin/bash
   echo "Running a basic Cloud Runner job"
   gsutil ls gs://<YOUR_BUCKET_NAME>/
   ```
2. **Run the job with Cloud Runner**:
   - Execute the script using Cloud Runner:
   ```bash
   cloud-runner run ./runner_script.sh
   ```
   - You should see the output of the files in your bucket.

### Step 6: Clean Up
1. **Delete the file from the bucket**:
   - To avoid incurring charges, delete the uploaded file:
   ```bash
   gsutil rm gs://<YOUR_BUCKET_NAME>/sample.txt
   ```
2. **Delete the bucket**:
   - If you no longer need the bucket, delete it:
   ```bash
   gsutil rb gs://<YOUR_BUCKET_NAME>
   ```

## Summary
In this lab, you created a GCP bucket, uploaded a file, and executed a basic job using Cloud Runner. This simple walkthrough helps you understand the basic functionality of Cloud Runner and GCP buckets.

Feel free to modify and extend this guide to include more advanced features.

## Next Steps
- Explore more advanced Cloud Runner jobs.
- Set up triggers to run jobs automatically based on events.
- Experiment with more GCP services like Cloud Functions or BigQuery.

