# **Lab 1: Data Storage and Warehouse using Google Cloud (GCP)**

---

## **Set Up Google Cloud Storage (GCS) Bucket**

### **What is GCS?**
Google Cloud Storage (GCS) is a scalable and secure storage service that lets you store any type of data and easily integrate with other Google services such as BigQuery, Machine Learning, and more.

---

### **Steps to Create a GCS Bucket:**

1. **Go to Google Cloud Console**:
    - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
    - On the left sidebar, scroll down to **Storage** and click on **Browser**.

2. **Create a New Bucket**:
    - Click on **Create Bucket**.
    - Assign a **unique name** to your bucket (e.g., `gcp-lab-bucket`).
    - For **Location**, choose `us-east1`.
    - Click **Create**.

3. **Set Permissions**:
    - Go to **IAM & Admin** in the console.
    - Under **Service Accounts**, click **Create Service Account**.
    - Name the service account (e.g., `lab1-service-account`), then select **Owner** role and click **Done**.

4. **Download Credentials**:
    - In the **Service Accounts** page, click the three dots (⋮) next to your service account and select **Manage Keys**.
    - Click **Add Key**, then **Create New Key** and choose **JSON**.
    - Download the JSON file and store it securely. This file will authenticate your Google Cloud project.

---

## **Step 1: Establish Connection from Local System to GCS Bucket**

In this step, you will connect your local machine to the GCS bucket to enable data storage.

### **Steps to Connect Local System to GCS Bucket:**

1. **Authenticate with GCP**:
   On your local machine, authenticate to Google Cloud by running:

   ```bash
   gcloud auth login
   ```

   This will open a web browser where you need to log in with your Google account.

2. **Set Your GCP Project**:
   Once authenticated, set the project that contains your GCS bucket:

   ```bash
   gcloud config set project <your-project-id>
   ```

   Replace `<your-project-id>` with the ID of your Google Cloud project.

3. **Install Google Cloud SDK** (if not already installed):
   - If you don't have the Google Cloud SDK installed on your local system, you can install it by following [this guide](https://cloud.google.com/sdk/docs/install).

4. **Verify Access to the GCS Bucket**:
   Test your access to the bucket by listing the contents (if any):

   ```bash
   gsutil ls gs://<your-bucket-name>
   ```

   Replace `<your-bucket-name>` with the actual name of your bucket (e.g., `gcp-lab-bucket`). If this returns no errors, your local system is now connected to the GCS bucket.

---

## **Step 2: Storing a Dataset in the GCS Bucket**

Now that the connection between your local system and GCS is set, you can store a dataset in the bucket. Let's add some additional features for better management of the data.

### **Steps to Upload Dataset to GCS Bucket:**

1. **Prepare the Dataset**:
   Assume you have a dataset named `dataset.csv` in a folder called `data`. First, make sure your dataset is in place:

   ```bash
   mkdir -p data
   mv <path-to-your-dataset> data/dataset.csv
   ```

2. **Upload the Dataset to GCS**:
   Using `gsutil`, you can upload your dataset to the GCS bucket:

   ```bash
   gsutil cp data/dataset.csv gs://<your-bucket-name>/data/dataset.csv
   ```

   This command uploads the `dataset.csv` file to the specified GCS bucket under the `data` folder.

3. **Enable Versioning on the GCS Bucket**:
   To track multiple versions of the dataset (useful for large-scale projects), enable object versioning on the GCS bucket:

   ```bash
   gsutil versioning set on gs://<your-bucket-name>
   ```

   With versioning enabled, GCS will maintain previous versions of the file when you update or overwrite it.

4. **Apply Object Lifecycle Management** (optional but recommended):
   You can configure lifecycle management policies for the objects in your bucket, such as deleting older versions after a certain number of days.

   - Create a lifecycle configuration file `lifecycle.json`:

     ```json
     {
       "rule": [
         {
           "action": {"type": "Delete"},
           "condition": {"age": 30}
         }
       ]
     }
     ```

   - Then apply it to the bucket:

     ```bash
     gsutil lifecycle set lifecycle.json gs://<your-bucket-name>
     ```

     This configuration will automatically delete any objects older than 30 days.

---

## **Track the Dataset with DVC (Optional)**

Since you already have DVC set up, you can track the dataset using DVC as follows :
(if you haven't set up DVCm you can find the steps under Labs--> Data Labs--> DVC_Labs)

```bash
dvc add data/dataset.csv
git add data/dataset.csv.dvc data/.gitignore
git commit -m "Track dataset with DVC"
dvc push
```

---

## **Access Your Dataset from GCS:**

To download or share the dataset later, you can use:

```bash
gsutil cp gs://<your-bucket-name>/data/dataset.csv ./data/dataset.csv
```

---

## **Additional Features:**

- **Encryption**: Ensure that your data is encrypted either with Google-managed keys or your own encryption keys.
- **Access Control**: Use GCS bucket policies and IAM roles to control who can access the data. You can grant access to specific users or service accounts.
- **Monitoring**: Enable logging and monitoring to track access patterns and any changes to your data over time using Google Cloud’s monitoring tools.

---

With these steps, your local system is now connected to the GCS bucket, and you can store and version datasets securely. Additionally, by enabling versioning and lifecycle management, you gain fine-grained control over how your data is stored and managed in the cloud.

