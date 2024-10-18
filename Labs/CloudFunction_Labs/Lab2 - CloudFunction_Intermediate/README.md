# Building a Serverless Machine Learning Pipeline with Google Cloud Functions


In this lab we will walk through the process of building a serverless machine learning pipeline using Google Cloud Functions, Pub/Sub, and Workflows and deploying individual functions for data processing, model training, and prediction, orchestrating them into a seamless pipeline. 


---

## Step 1: Enable Required APIs
To use Cloud Functions, Pub/Sub, Workflows, and Cloud Storage in this project, enable the corresponding APIs. 
Run the following command to enable them:

```bash
gcloud services enable \
    cloudfunctions.googleapis.com \
    pubsub.googleapis.com \
    workflows.googleapis.com \
    storage.googleapis.com \
    monitoring.googleapis.com
```
---
## Step 2: Create Pub/Sub Topics for Pipeline Stages
We will use Pub/Sub topics to manage communication between various pipeline stages. 

### What are Pub/Sub Topics?
Google Cloud Pub/Sub is a messaging service that allows for asynchronous communication between applications by 
decoupling the sender (publisher) and the receiver (subscriber) of messages. 

In this model:
- **Publishers** send messages to a topic.
- **Subscribers** receive those messages from the topic.

Each message published to a topic is automatically sent to all subscribers of that topic, enabling efficient communication across distributed services.

### **Why are Pub/Sub Topics Used in This Lab?**

1. **Decoupling Services**: By using Pub/Sub, the pipeline stages (data processing, model training, and model serving) are decoupled from one another. Each stage runs independently and can scale according to the workload without directly relying on the previous or next stage.
   
2. **Reliability**: Pub/Sub provides message durability and ensures reliable delivery, meaning that even if one of the pipeline stages is temporarily unavailable, the messages will be delivered once the service is ready again.

3. **Scalability**: As Pub/Sub handles the communication between pipeline stages, it allows each stage to scale independently based on incoming messages. For example, if a large amount of data is processed, multiple instances of the model training function can be triggered simultaneously.

4. **Asynchronous Processing**: The pipeline stages do not have to wait for one another to complete before starting the next stage. For example, the data processing function can trigger the model training stage once it finishes processing, without needing to wait for the model training to finish before other data processing tasks continue.



- **`data-processing-trigger`**: This topic triggers the data processing function when new data is available in the Cloud Storage bucket.
- **`model-training-trigger`**: This topic triggers the model training function once data processing is complete and the system is ready to train the model.
- **`model-serving-trigger`**: This topic triggers the model serving function to make predictions after the model has been successfully trained.

Create the following Pub/Sub topics:

```bash
gcloud pubsub topics create data-processing-trigger
gcloud pubsub topics create model-training-trigger
gcloud pubsub topics create model-serving-trigger
```
---
## Step 3: Deploy Cloud Functions for Pipeline Stages
We will create and deploy three Cloud Functions: one for data processing, one for model training, and one for model serving (prediction).

### 3.1 Data Processing Function
 
The function is triggered by a Cloud Storage event, which passes details about the newly uploaded file in the `event` object. This includes the bucket name and the file name, which the function uses to retrieve the uploaded data.
The function does not directly trigger the next pipeline stage. Instead, it publishes a message to a Pub/Sub topic, allowing the system to remain decoupled and scalable.

 Deploy the function as follows:
``` bash
gcloud functions deploy process_data \
    --runtime python310 \
    --trigger-resource YOUR_BUCKET_NAME \
    --trigger-event google.storage.object.finalize \
    --region us-central1
```
Replace YOUR_BUCKET_NAME with the name of the Cloud Storage bucket.

### 3.2 Model Training Function
The function is triggered by a Pub/Sub message that contains the file name of the dataset to be used for training. The message is encoded in base64, so the first step is to decode the message and extract the file name from the message data.
It retrieves the file from a specified Cloud Storage bucket using the `bucket` and `blob` objects.
It uploads the model file to the Cloud Storage bucket, making it accessible for the next stages of the pipeline, such as model serving (prediction).

```bash
gcloud functions deploy train_model \
    --runtime python310 \
    --trigger-topic model-training-trigger \
    --region us-central1 \
    --entry-point train_model \
    --timeout 540s \
    --memory 512MB
```
### 3.3 Model Serving (Prediction) Function
The `predict` function is responsible for serving predictions based on a pre-trained machine learning model. It handles HTTP requests, processes input data, and returns model predictions.
```bash
gcloud functions deploy ml_model_predict \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --region us-central1 \
    --entry-point predict \
    --timeout 60s \
    --memory 256MB
```
---
## Step 4: Create the Workflow
This workflow orchestrates the pipeline by coordinating the execution of the data processing, model training, and model prediction stages through HTTP requests to the corresponding Cloud Functions.

#### **1. Initiate Data Processing**
The first step (`initiate-data-processing`) triggers the `process_data` Cloud Function via an HTTP POST request:
- The request includes the `bucket` and `file` parameters to specify the Cloud Storage location where the data (`data.csv`) is stored.
- This step initiates the data processing function, which will clean and process the data, then publish a message to start model training.

#### **2. Initiate Model Training**
Once data processing is complete, the next step (`initiate-model-training`) triggers the `train_model` Cloud Function via another HTTP POST request:
- The request sends the file name (`data.csv`) as input.
- This step starts the training process using the processed data. The model is trained and then uploaded to Cloud Storage for future predictions.

#### **3. Initiate Model Serving (Prediction)**
After the model has been trained, the workflow moves to the model serving stage (`initiate-model-serving`) by calling the `ml_model_predict` function:
- It sends the input features for which the prediction is requested.
- The prediction function loads the pre-trained model from Cloud Storage and returns the prediction result.

#### **4. Return the Prediction**
The final step (`return_prediction`) captures the result from the model prediction step and returns it as the output of the workflow:
- The prediction result is extracted from the `model_prediction` variable, which contains the response body of the `ml_model_predict` function.

Deploy the workflow as follows:

```bash
gcloud workflows deploy mlops-workflow \
    --source=workflow.yaml \
    --location=us-central1
```
---

## Step 5: Test the Cloud Functions
Once the pipeline is set up, test the Cloud Functions with a simple curl request to the prediction function. Replace YOUR_PROJECT_ID with your actual Google Cloud project ID.

```bash
curl -X POST https://us-central1-YOUR_PROJECT_ID.cloudfunctions.net/ml_model_predict \
    -H "Content-Type: application/json" \
    -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```
This will send a request to the prediction function with an array of features. The function should return the predicted class.

