# **Google Cloud Platform Compute Engine - Lab 2**

## **Objective**
This lab focuses on intermediate-level skills in GCP Compute Engine, including creating custom VM images, using snapshots, working with instance templates and managed instance groups (MIGs), and configuring networking settings. Participants will set up a scalable sentiment analysis model deployment pipeline using FastAPI and leverage snapshots for disaster recovery.

## **Lab Steps**

### **Step 1: Create a Custom VM Image with Pre-installed Software**

1. **Create a VM instance:**
   - Go to the Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/).
   - Navigate to Compute Engine > VM instances.
   - Click "Create Instance".
   - Configure the instance:
     - Name: `custom-image-instance`
     - Region: `us-central1`
     - Zone: `us-central1-a`
     - Machine type: `e2-micro` (1 vCPU, 1 GB memory)
     - Boot disk: Debian GNU/Linux 10 (buster)
   - Click "Create".

2. **Install necessary software on the VM instance:**
   - SSH into the VM instance.
   - Install Python, pip, FastAPI, and Uvicorn:
     ```sh
     sudo apt update
     sudo apt install python3 python3-pip -y
     pip3 install fastapi uvicorn numpy pandas scikit-learn
     ```

3. **Create a custom image from the VM instance:**
   - Stop the VM instance.
   - Go to Compute Engine > Images.
   - Click "Create Image".
   - Configure the image:
     - Name: `custom-image`
     - Source: `Disk` > `custom-image-instance` boot disk
   - Click "Create".

### **Step 2: Create and Use a VM Snapshot**

1. **Create a snapshot of the VM instance:**
   - Start the VM instance you created earlier.
   - SSH into the VM and set up the FastAPI application and IMDb dataset (details in Step 5).
   - Stop the VM instance.
   - Go to Compute Engine > Snapshots.
   - Click "Create Snapshot".
   - Configure the snapshot:
     - Name: `custom-image-snapshot`
     - Source disk: `custom-image-instance` boot disk
   - Click "Create".

2. **Use the snapshot to restore the application in case of failure:**
   - Simulate a failure by deleting the VM instance.
   - Restore the snapshot to a new VM instance:
     - Go to Compute Engine > VM instances.
     - Click "Create Instance".
     - Select `New VM instance from snapshot`.
     - Choose the snapshot `custom-image-snapshot`.
     - Configure the instance:
       - Name: `restored-instance`
       - Region: `us-central1`
       - Zone: `us-central1-a`
       - Machine type: `e2-micro` (1 vCPU, 1 GB memory)
   - Click "Create".
   - Verify the restored instance has the FastAPI application and IMDb dataset.

### **Step 3: Configure Networking and Security**

1. **Set up VPC and subnets:**
   - Navigate to VPC Network > VPC Networks.
   - Click "Create VPC Network".
   - Configure the VPC:
     - Name: `mlops-vpc`
     - Subnet name: `mlops-subnet`
     - Region: `us-central1`
     - IP range: `10.0.0.0/24`
   - Click "Create".

2. **Set up firewall rules:**
   - Go to VPC Network > Firewall Rules.
   - Click "Create Firewall Rule".
   - Configure the rule:
     - Name: `allow-ssh-http-https`
     - Network: `mlops-vpc`
     - Targets: `All instances in the network`
     - Source IP ranges: `0.0.0.0/0`
     - Allowed protocols and ports:
       - tcp:22 (SSH)
       - tcp:80 (HTTP)
       - tcp:443 (HTTPS)
   - Click "Create".

### **Step 4: Create an Instance Template and Managed Instance Group (MIG)**

1. **Create an instance template:**
   - Navigate to Compute Engine > Instance Templates.
   - Click "Create Instance Template".
   - Configure the template:
     - Name: `mlops-template`
     - Machine type: `e2-micro` (1 vCPU, 1 GB memory)
     - Boot disk: Custom image `custom-image`
     - Network: `mlops-vpc`
   - Click "Create".

2. **Create a managed instance group (MIG):**
   - Go to Compute Engine > Instance Groups.
   - Click "Create Instance Group".
   - Configure the group:
     - Name: `mlops-mig`
     - Location: `Single zone`
     - Zone: `us-central1-a`
     - Instance template: `mlops-template`
     - Autoscaling policy:
       - Target CPU utilization: 60%
       - Minimum number of instances: 1
       - Maximum number of instances: 3
   - Click "Create".

### **Step 5: Deploy Sentiment Analysis Model with FastAPI**

1. **Download the IMDb dataset:**
   - The dataset can be downloaded from [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews).
   - Upload the dataset to the VM instance. You can use `scp` to transfer the file:
     ```sh
     scp -i path/to/private/key IMDb_Reviews.csv username@instance_external_ip:/home/username/
     ```

2. **Prepare the FastAPI script and dataset:**
   - SSH into a VM instance from the MIG.
   - Ensure the IMDb dataset is in the home directory or a known location.
   - Prepare the FastAPI script (e.g., `main.py`):
     ```python
     from fastapi import FastAPI
     from pydantic import BaseModel
     import pandas as pd
     from sklearn.feature_extraction.text import TfidfVectorizer
     from sklearn.linear_model import LogisticRegression

     app = FastAPI()

     # Load IMDb dataset
     data = pd.read_csv('IMDb_Reviews.csv')

     # Preprocess data
     X = data['review']
     y = data['sentiment']

     # Vectorize text data
     vectorizer = TfidfVectorizer(max_features=5000)
     X_train = vectorizer.fit_transform(X)
     model = LogisticRegression()
     model.fit(X_train, y)

     class Review(BaseModel):
         review: str

     @app.post("/predict/")
     def predict_sentiment(review: Review):
         X_new = vectorizer.transform([review.review])
         prediction = model.predict(X_new)
         return {"sentiment": prediction[0]}

     @app.get("/health")
     def health_check():
         return {"status": "ok"}

     if __name__ == "__main__":
         import uvicorn
         uvicorn.run(app, host="0.0.0.0", port=8000)
     ```

3. **Run the FastAPI server:**
   - Execute the script on the VM instance:
     ```sh
     uvicorn main:app --host 0.0.0.0 --port 8000
     ```

### **Step 6: Configure Load Balancer**

1. **Set up a load balancer:**
   - Navigate to Network Services > Load balancing.
   - Click "Create Load Balancer".
   - Select `HTTP(S) Load Balancing`.
   - Click `Start configuration`.

2. **Configure the backend service:**
   - **Step 1: Backend configuration**
     - Name: `mlops-backend`
     - Backend type: `Instance group`
     - Instance group: `mlops-mig`
     - Port: `80`
     - Click on `Create a health check`.
     - In the "Create a health check" dialog, configure the health check:
       - Name: `mlops-health-check`
       - Protocol: `HTTP`
       - Port: `80`
       - Request path: `/health`
       - Check interval: `5 seconds`
       - Timeout: `5 seconds`
       - Unhealthy threshold: `2`
       - Healthy threshold: `2`
     - Click `Save and continue`.
   - In the backend configuration screen, under Health check, select the health check you just created (`mlops-health-check`).
   - Click `Done`.

3. **Configure the frontend service:**
   - **Step 2: Frontend configuration**
     - Name: `mlops-frontend`
     - Protocol: `HTTP`
     - IP: `Ephemeral`
     - Port: `80`
     - Click `Done`.

4. **Configure the traffic distribution algorithm:**
   - **Step 3: Traffic distribution configuration**
     - Under `Advanced settings` in the backend service configuration, select the `Session affinity` to `None` (default round-robin algorithm) or choose another algorithm based on your requirements.

5. **Review and create the load balancer:**
   - **Step 4: Review**
     - Review your configuration.
     - Click `Create`.

### **Step 7: Simulate Load and Demonstrate Autoscaling**

1. **Simulate load on the MIG:**
   - Use a load testing tool (e.g., Apache JMeter, locust) to send multiple HTTP requests to the load balancer's IP to the `/predict/` endpoint.
   - Sample locust script:
     ```python
     from locust import HttpUser, TaskSet, task, between

     class UserBehavior(TaskSet):
         @task
         def predict(self):
             self.client.post("/predict/", json={"review": "This movie was fantastic!"})

     class WebsiteUser(HttpUser):
         tasks = [UserBehavior]
         wait_time = between(1, 2)

     if __name__ == "__main__":
         import os
         os.system("locust -f locustfile.py")
     ```

2. **Monitor autoscaling:**
   - Go to Compute Engine > Instance Groups.
   - Observe the number of instances in the MIG increasing as the load increases.
   - Verify that the MIG scales up when CPU utilization exceeds the threshold.

3. **Test the load balancer:**
   - Send HTTP requests to the load balancer's IP to the `/predict/` endpoint with sample reviews.
   - Verify the distribution of traffic and the performance of the sentiment analysis service.

---

By completing this lab, participants will gain hands-on experience with custom VM images, snapshots, instance templates, managed instance groups, and networking settings in GCP, applied to a practical ML project using FastAPI. They will also understand the importance of snapshots for disaster recovery by simulating a failure and restoring the application from a snapshot. Additionally, they will see how to configure and test a load balancer, ensuring traffic is evenly distributed across instances, and how autoscaling can dynamically adjust the number of instances based on load.
