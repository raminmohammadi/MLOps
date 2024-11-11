### Cloud Runner Intermediate Lab
Welcome to the intermediate Cloud Runner lab! In this lab, we will focus on managing data, setting up cloud infrastructure, and running analysis or machine learning workflows on Google Cloud.

---

### Updated Step-by-Step Guide

#### Step 1: Setting Up Google Cloud Project and Storage

1. **Create a Google Cloud Project**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and give it a name (e.g., `cloud_runner_lab`).
  
2. **Create a Google Cloud Storage Bucket**
   - Navigate to the **Cloud Storage** section.
   - Create a new bucket with a unique name (e.g., `cloud-runner-lab-bucket`).
   - Choose **Region** (e.g., `us-central1`) and **Storage Class** (e.g., Standard).
   - In the **Permissions** tab, add necessary roles (e.g., `Storage Admin`) to allow Cloud Runner access to this bucket.

3. **Enable Necessary APIs**
   - Go to **APIs & Services** > **Library**.
   - Enable the following APIs:
     - **Cloud Storage API**
     - **BigQuery API** (if you plan to use BigQuery)

#### Step 2: Configuring Cloud Runner

1. **Initialize Cloud Runner**
   - Run the following command in your terminal:
     ```bash
     cloud-runner init
     ```
   - Follow the prompts to authenticate and connect your Google Cloud account.

2. **Configure Project and Bucket Details**
   - Update the `cloud-runner-config.yaml` file with your project and bucket details:
     ```yaml
     project_id: "YOUR_PROJECT_ID"
     bucket_name: "YOUR_BUCKET_NAME"
     region: "us-central1"
     ```

3. **Test Cloud Runner Connection**
   - Run the following command to ensure Cloud Runner is connected:
     ```bash
     cloud-runner test
     ```
   - If any issues arise, verify that the `cloud-runner-config.yaml` file is correctly configured and that your Google Cloud authentication is active.

#### Step 3: Building a Data Pipeline

1. **Set Up Data Extraction Script**
   - In `pipeline/extract.py`, create a script to pull data from your source.
   - Save the extracted data into your Google Cloud Storage bucket.
   - **Example extraction code**:
     ```python
     import requests
     import cloud_runner

     def extract_data():
         url = "https://example.com/data.csv"
         response = requests.get(url)
         with open('data.csv', 'wb') as file:
             file.write(response.content)
         cloud_runner.upload_file('data.csv', bucket_name='YOUR_BUCKET_NAME')

     if __name__ == "__main__":
         extract_data()
     ```

2. **Preprocessing Data**
   - In `pipeline/preprocess.py`, write a script for data cleaning and transformation.
   - **Example preprocessing code**:
     ```python
     import pandas as pd
     import cloud_runner

     def preprocess_data():
         df = pd.read_csv('gs://YOUR_BUCKET_NAME/data.csv')
         # Transform data (e.g., drop missing values)
         processed_data = df.dropna()
         processed_data.to_csv('processed_data.csv', index=False)
         cloud_runner.upload_file('processed_data.csv', bucket_name='YOUR_BUCKET_NAME')

     if __name__ == "__main__":
         preprocess_data()
     ```

3. **Run the Pipeline**
   - Chain the extraction and preprocessing steps by running each script in sequence:
     ```bash
     cloud-runner run pipeline/extract.py
     cloud-runner run pipeline/preprocess.py
     ```

#### Step 4: Running Data Analysis

1. **Set Up Analysis Script**
   - In `pipeline/analyze.py`, write a script for data analysis or model training.
   - **Example analysis code**:
     ```python
     import pandas as pd
     import cloud_runner

     def analyze_data():
         df = pd.read_csv('gs://YOUR_BUCKET_NAME/processed_data.csv')
         result = df.describe()
         with open('analysis_results.txt', 'w') as f:
             f.write(result.to_string())
         cloud_runner.upload_file('analysis_results.txt', bucket_name='YOUR_BUCKET_NAME')

     if __name__ == "__main__":
         analyze_data()
     ```

2. **Run the Analysis Script**
   - Execute the analysis step:
     ```bash
     cloud-runner run pipeline/analyze.py
     ```

#### Step 5: Cleanup and Shutdown

1. **Clean Up Cloud Resources**
   - Delete temporary files from your Google Cloud Storage bucket:
     ```bash
     gsutil rm gs://YOUR_BUCKET_NAME/*.csv
     ```

2. **Deactivate Python Virtual Environment**
   - If you’re using a virtual environment, deactivate it:
     ```bash
     deactivate
     ```

---

### Lab Conclusion
Congratulations on completing the lab! You have successfully:

- Set up Google Cloud resources and configured access for Cloud Runner.
- Built and run a data pipeline, from data extraction to analysis, on the cloud.
- Managed cloud resources to ensure efficient usage.
