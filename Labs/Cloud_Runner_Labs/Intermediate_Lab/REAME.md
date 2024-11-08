# Cloud Runner Intermediate Lab

Welcome to the intermediate Cloud Runner lab! In this lab, we'll dive deeper into managing data, setting up cloud infrastructure, and running analysis or machine learning workflows on the cloud. This lab assumes basic familiarity with cloud environments, version control, and Python programming.

## Table of Contents

- [Objectives](#objectives)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
  - [Step 1: Setting Up Google Cloud Project and Storage](#step-1-setting-up-google-cloud-project-and-storage)
  - [Step 2: Configuring Cloud Runner](#step-2-configuring-cloud-runner)
  - [Step 3: Building a Data Pipeline](#step-3-building-a-data-pipeline)
  - [Step 4: Running Data Analysis](#step-4-running-data-analysis)
  - [Step 5: Cleanup and Shutdown](#step-5-cleanup-and-shutdown)
- [Lab Conclusion](#lab-conclusion)

---

## Objectives

By the end of this lab, you will:
- Set up Google Cloud Storage buckets and configure access controls.
- Configure Cloud Runner to interact with Google Cloud.
- Build and run an end-to-end data pipeline on the cloud.
- Execute data analysis or machine learning workflows.
- Learn to manage cloud resources efficiently to reduce costs.

## Prerequisites

Before you start, ensure you have:
1. **Google Cloud Account**: Make sure you have access to Google Cloud Console and billing enabled.
2. **Cloud Runner CLI**: Installed on your local machine.
3. **Basic knowledge of Python**: For data analysis and pipeline scripting.
4. **Git**: Installed and configured on your local machine.

## Step-by-Step Guide

### Step 1: Setting Up Google Cloud Project and Storage

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and name it appropriately (e.g., `cloud_runner_lab`).

2. **Create a Google Cloud Storage Bucket**
   - Go to the [Cloud Storage](https://console.cloud.google.com/storage) section.
   - Create a bucket with a unique name (e.g., `cloud-runner-lab-bucket`).
   - Set the **Region** and **Storage Class** based on your requirements (e.g., `us-central1` and `Standard`).
   - In the **Permissions** tab, add necessary roles (e.g., `Storage Admin`) to allow Cloud Runner access to this bucket.

3. **Enable Necessary APIs**
   - Enable the following APIs:
     - Cloud Storage API
     - BigQuery API (if data warehousing is required)

### Step 2: Configuring Cloud Runner

1. **Initialize Cloud Runner**
   - Run the following command to initialize Cloud Runner and authenticate your Google Cloud account.

   ```bash
   cloud-runner init
   ```

2. **Configure Project and Bucket Details**
   - Update the `cloud-runner-config.yaml` file in the root directory with your project and bucket details.

   ```yaml
   project_id: "YOUR_PROJECT_ID"
   bucket_name: "YOUR_BUCKET_NAME"
   region: "us-central1"
   ```

3. **Test Cloud Runner Connection**
   - Test the connection to ensure Cloud Runner can interact with your bucket.

   ```bash
   cloud-runner test
   ```

### Step 3: Building a Data Pipeline

1. **Set Up Data Extraction Script**
   - In the `pipeline/extract.py` file, write a script to pull data from your source (e.g., a public dataset or API).
   - Save extracted data into your Google Cloud Storage bucket.

   ```python
   # Example extraction code in extract.py
   import requests
   import cloud_runner

   def extract_data():
       url = "https://example.com/data"
       response = requests.get(url)
       with open('data.csv', 'wb') as file:
           file.write(response.content)
       cloud_runner.upload_file('data.csv', 'YOUR_BUCKET_NAME')
   ```

2. **Preprocessing Data**
   - In `pipeline/preprocess.py`, create a preprocessing script to clean and transform the data.

   ```python
   # Example preprocessing code in preprocess.py
   import pandas as pd
   import cloud_runner

   def preprocess_data():
       df = pd.read_csv('gs://YOUR_BUCKET_NAME/data.csv')
       # Perform transformations
       processed_data = df.dropna()  # Example transformation
       cloud_runner.upload_file(processed_data, 'YOUR_BUCKET_NAME', 'processed_data.csv')
   ```

3. **Run the Pipeline**
   - Chain the extraction and preprocessing scripts and run them via Cloud Runner.

   ```bash
   cloud-runner run pipeline/extract.py
   cloud-runner run pipeline/preprocess.py
   ```

### Step 4: Running Data Analysis

1. **Set Up Analysis Script**
   - Write an analysis script in `pipeline/analyze.py` that performs data analysis or trains a model on the processed data.
   - Save the results or model in Google Cloud Storage.

   ```python
   # Example analysis code in analyze.py
   import pandas as pd

   def analyze_data():
       df = pd.read_csv('gs://YOUR_BUCKET_NAME/processed_data.csv')
       # Perform analysis or train model
       result = df.describe()  # Example summary stats
       with open('analysis_results.txt', 'w') as f:
           f.write(result.to_string())
       cloud_runner.upload_file('analysis_results.txt', 'YOUR_BUCKET_NAME')
   ```

2. **Run the Analysis Script**
   - Execute the analysis step with Cloud Runner.

   ```bash
   cloud-runner run pipeline/analyze.py
   ```

### Step 5: Cleanup and Shutdown

1. **Clean Up Cloud Resources**
   - Delete any temporary files from your bucket if they are no longer needed.

   ```bash
   gsutil rm gs://YOUR_BUCKET_NAME/*.csv
   ```

2. **Deactivate Virtual Environment**
   - When finished, deactivate your Python virtual environment.

   ```bash
   deactivate
   ```

## Lab Conclusion

Congratulations! You have completed the Cloud Runner Intermediate Lab. You have learned to:
- Set up Google Cloud resources and configure access for Cloud Runner.
- Build a cloud-based data pipeline with data extraction, preprocessing, and analysis.
- Clean up resources to ensure cost efficiency.

Feel free to expand this pipeline with more complex data processing or model training tasks! For any issues, please reach out in the Issues section.
```
