# ETL Pipeline: Google Cloud Storage to BigQuery using Cloud Functions

In this lab we will walk through setting up an automated ETL pipeline to transfer data from a Google Cloud Storage bucket to BigQuery using Cloud Functions.


---

## Step 1: Enable Cloud Functions API

1. Go to the **Google Cloud Console**.
2. Navigate to **APIs & Services** > **Library**.
3. Search for **Cloud Functions API** and click **Enable**.

---

## Step 2: Create a Google Cloud Storage Bucket

1. In the Google Cloud Console, navigate to **Storage** > **Buckets**.
2. Click **Create Bucket**.
3. Choose a globally unique name for your bucket (e.g., `my-etl-bucket`).
4. Set the location type to **Region** and choose the region (e.g., `us-central1`). Ensure that the Cloud Function will be created in the same region.
5. Leave all other options as default and click **Create**.

---

## Step 3: Set Up IAM Roles for the Service Account

1. Navigate to **IAM & Admin** > **IAM**.
2. Locate the **default Compute Service Account** (usually in the format `PROJECT_NUMBER-compute@developer.gserviceaccount.com`).
3. Assign the following roles to the service account:
   - **BigQuery Admin**: Allows the service account to create and manage BigQuery tables.
   - **Eventarc Event Receiver**: Required to trigger Cloud Functions based on Google Cloud Storage events.

---

## Step 4: Create a Cloud Function

1. In the Google Cloud Console, navigate to **Cloud Run Functions**.
2. Click **Create Function**.
3. Configure the following settings:
   - **Name**: Provide a name for the function (e.g., `etl-function`).
   - **Region**: Select the region (ensure it matches the region of your storage bucket).
   - **Trigger**: 
     - Set the trigger type to **Cloud Storage**.
     - Set the **Event Type** to `google.cloud.storage.object.v1.finalized` (this triggers the function when a file is finalized in the bucket).
     - Select the storage bucket you created (e.g., `my-etl-bucket`).

4. Click **Next** to proceed to the runtime configuration.

---

## Step 5: Configure Runtime and Code

1. In the **Runtime** tab, configure the following:
   - **Runtime**: Select **Python 3.11**.
   - **Entry point**: Provide the entry point function name from your `main.py` file (e.g., `hello_gcs`).
   
2. Upload the following files:
   - **main.py**: This will contain the main logic to handle the ETL process.
   - **requirements.txt**: List any dependencies such as `google-cloud-storage` and `google-cloud-bigquery`.
   - **schemas.yaml**: Define the schema of the BigQuery table.

###  `main.py`

- **streaming(data)**: This function is triggered when a file is uploaded to the storage bucket. It checks the file's name, determines the schema using the schemas.yaml configuration, and initiates the process of loading data into BigQuery.

- **_check_if_table_exists(tableName, tableSchema)**: This function ensures that the corresponding BigQuery table exists, and if not, creates it.

- **_load_table_from_uri(bucket_name, file_name, tableSchema, tableName)**: This function is responsible for loading the data from the Google Cloud Storage URI into the specified BigQuery table. It uses bigquery.LoadJobConfig to define how the data is loaded (in this case, the source format is NEWLINE_DELIMITED_JSON).

- **create_schema_from_yaml(table_schema)**: This function takes the schema defined in schemas.yaml and converts it into BigQuery schema fields. It supports nested fields (RECORD types) as well.

- **hello_gcs(cloud_event)**: This is the entry point for the Cloud Function. It is triggered by a new file being uploaded to the Google Cloud Storage bucket. It logs the event metadata and invokes the streaming() function to process the data and load it into BigQuery.

## Step 6: Create a BigQuery Dataset
1. In the Google Cloud Console, navigate to **BigQuery**.
2. Under your project, click Create Dataset.
3. Name the dataset staging (as used in the main.py file).
4. Click Create.

## Step 7: Test the ETL Pipeline
1. Go to the Google Cloud Console and navigate to Storage.
2. Upload a sample JSON file to the bucket (e.g., data.json).
3. Navigate to Cloud Functions > Logs and check if the function ran successfully.
4. Go to BigQuery and query the staging dataset to ensure that the table was created and the data was inserted.

---

# ML Model Example (HTTP Triggered Cloud Function)
## Step 1: Create a New Function
1. In the Google Cloud Console, navigate to Cloud Run Functions.
2. Click Create Function.
3. Configure the following:

   - Name: Provide a name for the function (e.g., ml-model-function).
   - Region: Select your region.
   - Trigger: Select HTTP trigger and allow unauthenticated users.
4. Click Next to proceed to the runtime configuration.

## Step 2: Upload the Model Code
1. Set Python 3.11 as the runtime.
2. Upload your main.py and requirements.txt files that define the machine learning model and logic to make predictions.