Here's a step-by-step intermediate lab for **Data Storage and Warehouse** that you can add to GitHub, based on your existing labs but with additional functionalities and complexity:

### Lab Title: **Intermediate Lab - Automating Data Ingestion and Querying in GCP using BigQuery and Cloud Storage**

---

### Objective:
In this lab, students will learn how to:
1. Set up automated data ingestion into a Google Cloud Storage bucket.
2. Configure a Pub/Sub notification to trigger a Cloud Function when new data is uploaded.
3. Load the uploaded data automatically into BigQuery using the Cloud Function.
4. Write queries in BigQuery to analyze the ingested data.

### Prerequisites:
- Google Cloud Platform (GCP) account with permissions for Cloud Storage, BigQuery, Cloud Pub/Sub, and Cloud Functions.
- Familiarity with basic GCP services, especially Cloud Storage and BigQuery.
- Completion of the beginner lab (creating a GCP bucket, loading data, running simple BigQuery queries).

---

### Steps:

---

#### 1. **Create a New Cloud Storage Bucket**
   - Go to the GCP Console.
   - In the **Storage** section, create a new bucket.
   - Set the storage class to **Standard** and choose the region closest to your users.
   - Ensure the bucket is public (or define appropriate permissions).
   
   **Command (using gcloud CLI)**:
   ```bash
   gsutil mb -l <REGION> gs://<BUCKET_NAME>/
   ```

---

#### 2. **Upload a File to the Bucket (Simulated Data Upload)**
   - Upload a CSV file or any dataset to the created bucket.
   - This dataset will simulate new data being uploaded by a user.

   **Command**:
   ```bash
   gsutil cp <LOCAL_FILE_PATH> gs://<BUCKET_NAME>/
   ```

---

#### 3. **Set Up a Cloud Pub/Sub Notification for New File Uploads**
   - Create a **Pub/Sub** topic that will act as a trigger whenever new data is uploaded to the bucket.
   - In the **Storage** section of the GCP Console, go to your bucket, click on **Edit notifications**, and link it to the newly created Pub/Sub topic.

   **Steps**:
   1. Navigate to **Pub/Sub** in GCP.
   2. Create a **Topic** named `data-ingestion-topic`.
   3. Go back to your bucket, select **Notifications**, and link it to the `data-ingestion-topic`.

---

#### 4. **Create a Cloud Function to Load Data into BigQuery**
   - Create a **Cloud Function** that will be triggered by the Pub/Sub topic.
   - The function will load the data from the uploaded file into a BigQuery table.

   **Python code for Cloud Function**:
   ```python
   import json
   from google.cloud import storage, bigquery

   def load_to_bigquery(event, context):
       """Triggered by a Pub/Sub message when a file is uploaded to Cloud Storage."""
       
       client = storage.Client()
       bucket_name = event['attributes']['bucketId']
       file_name = event['attributes']['objectId']
       
       dataset_id = 'your_dataset_id'
       table_id = 'your_table_id'
       uri = f'gs://{bucket_name}/{file_name}'
       
       bigquery_client = bigquery.Client()
       dataset_ref = bigquery_client.dataset(dataset_id)
       table_ref = dataset_ref.table(table_id)
       
       job_config = bigquery.LoadJobConfig(
           autodetect=True,
           source_format=bigquery.SourceFormat.CSV
       )
       
       load_job = bigquery_client.load_table_from_uri(
           uri, table_ref, job_config=job_config
       )
       
       load_job.result()  # Wait for the job to complete.
       print(f'Loaded {file_name} into {table_id}')
   ```

   **Steps to Create Cloud Function**:
   1. Go to **Cloud Functions**.
   2. Click **Create Function** and choose **HTTP** as the trigger type.
   3. Set the memory and timeout appropriately.
   4. Write the function code in Python.
   5. In the **Trigger** section, link the function to the `data-ingestion-topic`.

---

#### 5. **Create a BigQuery Table and Dataset**
   - In BigQuery, create a dataset (if you haven't already) where the data will be stored.
   - Create a table within that dataset. You can use schema autodetection when loading the data.

   **Command**:
   ```bash
   bq mk --dataset <PROJECT_ID>:<DATASET_NAME>
   ```

---

#### 6. **Test the Automated Data Pipeline**
   - Upload a new file to the Cloud Storage bucket.
   - Check the logs in **Cloud Functions** to ensure that the function was triggered successfully.
   - Verify that the data has been loaded into BigQuery by querying the table in the BigQuery console.

   **Query Example**:
   ```sql
   SELECT * FROM `<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>`
   ```

---

#### 7. **Extend the Lab - Querying and Data Transformation**
   - Ask students to write advanced queries using the ingested data.
   - Example tasks:
     - Write queries to filter specific rows based on conditions.
     - Perform data aggregation (e.g., finding averages, counts, or sums of columns).
     - Use Google Data Studio or Looker Studio to visualize the data.

   **Example Query**:
   ```sql
   SELECT category, AVG(sales) as avg_sales
   FROM `<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>`
   GROUP BY category
   ```

---

### Conclusion:
- This lab helps students automate the data pipeline from Cloud Storage to BigQuery.
- Students will also practice querying the loaded data and potentially visualize it.

### Deliverables:
- Upload this intermediate lab guide and the corresponding Python script to your GitHub repository.
- Record a video tutorial walking through the process and upload it to the appropriate platform (Google Drive/YouTube).
  
---

Let me know if you need further clarification or adjustments!
