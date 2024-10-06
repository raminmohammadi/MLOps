### **BigQuery Lab: MLOps Pipeline Using BigQuery and Cloud Functions**

---

### **Step 1: Setting Up the Environment**
1. **Create a New GCP Project:**
   - Log into **Google Cloud Platform (GCP)** and create a new project.
   - Enable the following APIs:
     - **BigQuery**
     - **Google Cloud Storage**
     - **Cloud Functions**

2. **Create a Service Account:**
   - Create a service account and give it permissions for BigQuery and Cloud Functions.
   - Download the service account key for authentication.

---

### **Step 2: Data Preparation and Ingestion**
1. **Download the Dataset:**
   - Download a simple dataset in CSV format (e.g., a sales or e-commerce dataset with columns such as `customer_id`, `total_sales`, `purchase_date`).

2. **Upload the Dataset to Google Cloud Storage:**
   - Create a **Cloud Storage bucket** and upload the dataset.
   - Ensure the bucket is accessible to BigQuery and Cloud Functions.

3. **Ingest Data into BigQuery:**
   - Use BigQuery’s UI or a SQL query to load the CSV file from Cloud Storage into BigQuery.
   - For example:
     ```sql
     CREATE OR REPLACE TABLE `your_project.your_dataset.sales_data`
     AS
     SELECT * FROM `your_bucket/sales_data.csv`;
     ```

---

### **Step 3: Automate Data Ingestion with Cloud Functions**
1. **Create a Cloud Function for Automation:**
   - Write a Cloud Function that listens for new file uploads in Cloud Storage and automatically ingests them into BigQuery.
   - Example Python function:
     ```python
     from google.cloud import bigquery

     def ingest_data(event, context):
         client = bigquery.Client()
         uri = f"gs://{event['bucket']}/{event['name']}"
         table_id = "your_project.your_dataset.sales_data"
         job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV)
         client.load_table_from_uri(uri, table_id, job_config=job_config).result()
     ```

2. **Deploy the Cloud Function:**
   - Deploy the Cloud Function in GCP with a Pub/Sub trigger that activates whenever a new file is uploaded to the bucket.

3. **Test the Function:**
   - Upload a new file to the Cloud Storage bucket and verify that the function ingests it into the BigQuery table.

---

### **Step 4: Train a Model Using BigQuery ML**
1. **Prepare the Data for Training:**
   - Use BigQuery SQL to clean and prepare the dataset for training a simple machine learning model:
     ```sql
     SELECT *, 
            CASE 
              WHEN total_sales > 500 THEN 'high_value'
              ELSE 'low_value'
            END AS sales_category
     FROM `your_project.your_dataset.sales_data`;
     ```

2. **Train a Model with BigQuery ML:**
   - Use **BigQuery ML** to train a **classification model** that predicts high- or low-value customers:
     ```sql
     CREATE OR REPLACE MODEL `your_project.your_dataset.customer_value_model`
     OPTIONS(model_type = 'logistic_reg') AS
     SELECT total_sales, customer_age, sales_category
     FROM `your_project.your_dataset.sales_data`
     WHERE sales_category IS NOT NULL;
     ```

3. **Evaluate the Model:**
   - Use **ML.EVALUATE** to check the model’s accuracy and other performance metrics:
     ```sql
     SELECT * FROM ML.EVALUATE(MODEL `your_project.your_dataset.customer_value_model`);
     ```

---

### **Step 5: Automate Model Retraining with Cloud Scheduler**
1. **Set Up Cloud Scheduler for Automation:**
   - Use **Cloud Scheduler** to trigger the Cloud Function daily (or on any schedule) to automatically check for new data and retrain the model with BigQuery ML.

2. **Cloud Function for Retraining:**
   - Modify your Cloud Function to trigger the model training query after the new data is ingested:
     ```python
     def retrain_model(event, context):
         client = bigquery.Client()
         query = '''
         CREATE OR REPLACE MODEL `your_project.your_dataset.customer_value_model`
         OPTIONS(model_type = 'logistic_reg') AS
         SELECT total_sales, customer_age, sales_category
         FROM `your_project.your_dataset.sales_data`
         WHERE sales_category IS NOT NULL;
         '''
         client.query(query).result()
     ```

3. **Deploy and Test:**
   - Deploy the updated function and test that the function triggers model retraining on schedule.

---

### **Step 6: Batch Predictions with BigQuery ML**
1. **Generate Predictions:**
   - Use **ML.PREDICT** to generate predictions on new customer data:
     ```sql
     SELECT customer_id, predicted_label
     FROM ML.PREDICT(MODEL `your_project.your_dataset.customer_value_model`, 
     (SELECT customer_id, total_sales, customer_age 
      FROM `your_project.your_dataset.sales_data`));
     ```

2. **Store Predictions in BigQuery:**
   - Save the predictions into a separate table for further analysis:
     ```sql
     CREATE OR REPLACE TABLE `your_project.your_dataset.customer_predictions` AS
     SELECT customer_id, predicted_label
     FROM ML.PREDICT(MODEL `your_project.your_dataset.customer_value_model`, 
     (SELECT customer_id, total_sales, customer_age 
      FROM `your_project.your_dataset.sales_data`));
     ```

---

### **Step 7: Monitoring and Visualization**
1. **Use Google Data Studio for Monitoring:**
   - Connect **Google Data Studio** to BigQuery to create a dashboard displaying:
     - Customer value predictions
     - Model performance metrics (accuracy, precision)
     - Ingestion status and new data insights

2. **Monitor the Model:**
   - Track performance over time and set up alerts for model degradation (if accuracy drops below a threshold).
