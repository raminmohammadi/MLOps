# Cloud Runner Basic Lab

Welcome to the beginners lab on Google Cloud Run! In this lab, you will learn to deploy a containerized application on Google Cloud Run, monitor its performance, and scale it based on traffic needs.

---

## Step-by-Step Guide

### Step 1: Set Up Google Cloud Project

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and give it a meaningful name (e.g., `cloud_runner_lab`).

2. **Enable Necessary APIs**:
   - In the Console, navigate to `APIs & Services > Library`.
   - Enable the **Cloud Run API** and the **Container Registry API**.

---

### Step 2: Create and Containerize the Application

1. **Create a Simple Flask Application**:
   - Write a basic Flask application in Python to use as your project.
   - Example `app.py`:
     ```python
     from flask import Flask

     app = Flask(__name__)

     @app.route('/')
     def hello_world():
         return "Hello, World!"

     if __name__ == "__main__":
         app.run(host="0.0.0.0", port=8080)
     ```

2. **Create a Dockerfile**:
   - In the same directory as your Flask app, create a Dockerfile to containerize the application.
   - Example Dockerfile:
     ```Dockerfile
     FROM python:3.8-slim

     WORKDIR /app
     COPY . /app
     RUN pip install flask

     EXPOSE 8080
     CMD ["python", "app.py"]
     ```

3. **Build the Docker Image**:
   - Ensure Docker is running on your local machine.
   - In the terminal, navigate to the app’s directory and build the Docker image:
     ```bash
     docker build -t gcr.io/YOUR_PROJECT_ID/hello-world .
     ```

---

### Step 3: Push the Docker Image to Container Registry

1. **Authenticate with Google Cloud**:
   - Set up authentication with Google Cloud using the following command:
     ```bash
     gcloud auth configure-docker
     ```

2. **Push the Docker Image**:
   - Tag and push your Docker image to the Container Registry:
     ```bash
     docker tag gcr.io/YOUR_PROJECT_ID/hello-world gcr.io/YOUR_PROJECT_ID/hello-world
     docker push gcr.io/YOUR_PROJECT_ID/hello-world
     ```

---

### Step 4: Deploy to Google Cloud Run

1. **Navigate to Cloud Run in Google Console**:
   - Go to the **Cloud Run** service in the Google Cloud Console.
   - Click **Create Service**.

2. **Configure the Deployment**:
   - Select **Deploy a container image** and choose the image you pushed to the Container Registry.
   - Set the **Region** (e.g., `us-central1`) and provide a **Service name**.
   - For **Authentication**, select "Allow unauthenticated invocations" if you want the app to be publicly accessible.

3. **Deploy the Application**:
   - Click **Create** to deploy the service. This process may take a few minutes.
   - Once deployed, Cloud Run will provide a URL for your application.

---

### Step 5: Access and Test the Application

- **Access the URL** provided by Cloud Run to test your application.
- You should see the message "Hello, World!" displayed if everything is working correctly.

---

### Step 6: Monitor and Scale the Service

1. **Monitor Metrics**:
   - Use the Cloud Run Console to monitor various metrics such as request count, response latency, and memory usage.
   - These metrics help you understand traffic and performance patterns.

2. **Auto-Scaling**:
   - Cloud Run automatically scales your service based on incoming traffic.
   - You can configure the minimum and maximum number of instances if needed to control scaling.

---

## Conclusion

Congratulations on completing the Cloud Runner Basic Lab! In this lab, you:

- Set up a Google Cloud project and enabled necessary APIs.
- Created and containerized a Flask application.
- Deployed it to Google Cloud Run and accessed it via a public URL.
- Monitored and scaled the service based on demand.

This lab provided a foundational understanding of Google Cloud Run and how to deploy containerized applications in a serverless environment. Enjoy exploring more with Google Cloud!
