Here is the revised lab guide, focusing only up to **How to query data in BigQuery using SQL**:

---

# **Lab 2: Data Warehousing using Google Cloud (GCP)**

---

## **Introduction to Google BigQuery**

### **What is Google BigQuery?**
Google BigQuery is a fully-managed, serverless data warehouse solution by Google Cloud. It allows you to store and analyze large datasets efficiently using SQL queries. BigQuery is designed to handle large-scale data analytics and can process billions of rows in just a few seconds.

---

## **Step 1: Set Up BigQuery in Google Cloud Console**

### **Steps to Set Up BigQuery:**

1. **Go to Google Cloud Console**:
    - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).

2. **Enable the BigQuery API**:
    - From the **Navigation Menu** on the left, scroll down and select **BigQuery** under the **Big Data** section.
    - If this is your first time using BigQuery, you may be prompted to enable the BigQuery API. Click **Enable**.

3. **Create a New BigQuery Dataset**:
    - Once in BigQuery, you will see your project listed in the explorer pane on the left side.
    - Click on your project, then click the **Create Dataset** button.
    - Name your dataset (e.g., `lab2_dataset`), choose a **data location** (e.g., `us-east1`), and leave the other settings as default.
    - Click **Create Dataset**.

---

## **Step 2: Load Data into BigQuery**

### **What is Data Loading in BigQuery?**
Loading data into BigQuery means taking data from a file (e.g., CSV) stored in a source like Google Cloud Storage (GCS) and uploading it to a BigQuery table so that you can analyze it using SQL.

In this step, you will load data from a CSV file into a table in BigQuery.

### **Steps to Load Data into BigQuery:**

1. **Prepare Your Dataset**:
   - You should already have your dataset uploaded to a Google Cloud Storage bucket (as covered in the previous lab).
   - For example, let’s assume your dataset is stored as `gs://<your-bucket-name>/data/dataset.csv`.

2. **Create a BigQuery Table**:
    - In the BigQuery Console, under your dataset, click on **Create Table**.
    - **Source**: For **Source**, choose **Google Cloud Storage**.
    - **File Path**: In the **URI** field, enter the path to your file (e.g., `gs://<your-bucket-name>/data/dataset.csv`).
    - **File Format**: Choose `CSV` as the file format.
    - **Table Name**: Name your table (e.g., `lab2_table`).
    - **Schema**: Select **Auto Detect** if you want BigQuery to automatically determine the schema, or enter the schema manually by specifying field names and data types.
    - Click **Create Table** to load the data into BigQuery.

---

## **Step 3: Querying Data in BigQuery**

### **What is Querying in BigQuery?**
Querying in BigQuery is similar to writing SQL queries to retrieve specific data from your dataset. Once the data is loaded, you can run SQL queries to perform operations like filtering, aggregating, or summarizing the data.

### **Steps to Query Data in BigQuery:**

1. **Go to BigQuery Editor**:
    - Once the data is loaded, you can query the table directly in BigQuery's SQL editor.

2. **Write a Basic Query**:
   - Here’s a simple SQL query that selects the first 10 rows from the table:

    ```sql
    SELECT * FROM `<your-project-id>.<lab2_dataset>.<lab2_table>` LIMIT 10;
    ```

    - Replace `<your-project-id>`, `<lab2_dataset>`, and `<lab2_table>` with your actual project, dataset, and table names.

3. **Run the Query**:
    - Click the **Run** button in the SQL editor.
    - BigQuery will process the query and return the results in seconds.

---

## **Conclusion**

By completing this lab, you have learned the following:
1. How to create a BigQuery dataset and table.
2. How to load data from Google Cloud Storage into BigQuery.
3. How to query data in BigQuery using SQL.

BigQuery is a powerful tool for handling large-scale data analytics, and this lab provides the foundational skills needed to start working with BigQuery on real-world datasets.

