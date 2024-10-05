# Pipelines with AutoML and Pre-built Containers

In this lab, we'll explore how to create end-to-end pipelines and get online predictions in Vertex AI.
Two ways discussed here are:
- Using AutoML
- Using Pre-built containers

## 1. End-to-End using AutoML

Dataset used is https://www.kaggle.com/datasets/taweilo/mba-admission-dataset

**Steps:**
- Dataset creation
- Train Model with AutoML
- Evaluate and Deploy the model to Endpoint
- Get online prediction using REST

###  Create a Dataset
**From the Console:**
- Go to Vertex AI
- Selected `Datasets`
- Select `CREATE DATASET`

<img width="1512" alt="Screenshot 2024-10-03 at 9 38 11 AM" src="https://github.com/user-attachments/assets/0090b98e-6093-4c91-97ad-4c80e4271ee1">

- Name the dataset MBA_data
- Select `Tabular and Regression/classification`
  - More on Model Types
- Click `Create`

<img width="1510" alt="Screenshot 2024-10-03 at 9 54 34 AM" src="https://github.com/user-attachments/assets/f4a3314b-67e7-4a2a-83b1-2e63b5eca8a6">

- Choose `Select CSV files from Cloud Storage`
- Copy `gsutil URI` of the data file from your "Cloud Storage" -> "Buckets" in the `Import file path`
- Click `CONTINUE`
<img width="1499" alt="Screenshot 2024-10-03 at 9 57 03 AM" src="https://github.com/user-attachments/assets/66fd7ca3-6a7c-4413-a2dd-4035ab3eea97">

- `Analyze` tab gives statistics about your data

<img width="1504" alt="Screenshot 2024-10-03 at 10 17 39 AM" src="https://github.com/user-attachments/assets/093bf0df-220a-4f2f-9963-cdfd59381f00">

- MBA_data is ready in your Datasets

### Train model with AutoML

On the Vertex AI console select `Training`:
Next to Training (near the top), select CREATE

- For Dataset enter MBA_data
- For Objective make sure Classification is selected
- Use AutoML for the method
- Click CONTINUE

<img width="1503" alt="Screenshot 2024-10-03 at 10 22 30 AM" src="https://github.com/user-attachments/assets/d8884db5-33f1-481c-9861-bea3d35cad47">

For Model Details:

- Here I'm giving the model name "vai-lab2"
- For Target column select the column to train predictions for
- Expand ADVANCED OPTIONS:
- You can select the split of training, test and validation for your data. Here I'll keep it Random which is default
- clicl `Continue`

  <img width="1505" alt="Screenshot 2024-10-03 at 10 27 31 AM" src="https://github.com/user-attachments/assets/b404847a-3e57-42c8-aaed-7e6a085a4026">

  **For Training options:**

- Click the - symbol next to any rows for variables that should be excluded from training, like the transaction_id
- More on Adavanced Options:
  - Model Weights
  - Optimization Objectives
- Pick AUC PR (Due to imbalance in Class)
- Click CONTINUE

<img width="1497" alt="Screenshot 2024-10-03 at 10 40 22 AM" src="https://github.com/user-attachments/assets/a8b9fcb8-4c19-489b-a1db-00c499bffa0d">

**For Compute and pricing:**

- Enter a Budget of 3 node hour
- Make sure Enable early stopping is toggled on
- Click `START TRAINING`

<img width="1495" alt="Screenshot 2024-10-03 at 10 41 29 AM" src="https://github.com/user-attachments/assets/fe7a4096-3b43-4c6b-bbc0-9688ab7e9e97">

### Model: Evaluate & Deploy

On the Vertex AI console, select `Models`


<img width="1493" alt="Screenshot 2024-10-03 at 5 35 36 PM" src="https://github.com/user-attachments/assets/5175768e-a8af-465f-aa54-2d33c1a152ce">

Select the model that was just trained MBA_data:

This brings up the EVALUATE tab for the model

(Changing your loss function can result in better results)

<img width="1496" alt="Screenshot 2024-10-03 at 5 37 34 PM" src="https://github.com/user-attachments/assets/f71135f8-2359-4d52-9da9-d0adf27a3234">

Select the tab labeled `DEPLOY & TEST`:

<img width="1497" alt="Screenshot 2024-10-03 at 5 45 20 PM" src="https://github.com/user-attachments/assets/4a5c19b9-4efa-4563-9245-80a060f4bd41">

In the Deploy to endpoint menus, complete Define your endpoint:

- For Endpoint name use MBA_endpoint
- keep defaults for `location and Access`
- Select `CONTINUE`

<img width="1503" alt="Screenshot 2024-10-03 at 5 49 18 PM" src="https://github.com/user-attachments/assets/54d382b6-d727-43cc-8683-3cbed683b94e">

Leave next model settings as default settings

Model monitoring and model objectives should be selected as required

<img width="1487" alt="Screenshot 2024-10-05 at 12 00 25 AM" src="https://github.com/user-attachments/assets/19803f8b-da25-4d21-8d53-99d5e9b8ddf4">

Here you can see the MBA_data endpoint is `active`, if you scroll the tab to left you can find `SAMPLE_REQUEST` that shows commands to get a URL link for online prediction either via REST or PYTHON with the deployed model.

<img width="1491" alt="Screenshot 2024-10-05 at 12 23 38 AM" src="https://github.com/user-attachments/assets/e7043deb-5f9f-44f6-a0e2-2a57a0da52ec">

The GCP interface has this feature where you can test if the deployed model on endpoint is working or not by giving the inputs without having to run the " curl  -POST " command directly in the same "DELPOY & TEST" page

<img width="1507" alt="Screenshot 2024-10-05 at 12 27 13 AM" src="https://github.com/user-attachments/assets/0cfe63ed-15eb-4cba-a6b0-28421946389e">


Now if you run the commands shown in `SAMPLE REQUEST` you'll get a URL similar to 
`https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict`

Now to actually send data to this model and get predictions, you can copy and paste this link into POSTMAN application.

To run this you'll need an access token to your GCP, which you'll get it by running this command `gcloud auth print-access-token`
in Google cloud shell

Use this token as authorization in the POSTMAN application and give your data in the format specified in the `SAMPLE REQUEST` to get your prediction.

<img width="1497" alt="Screenshot 2024-10-05 at 12 54 12 AM" src="https://github.com/user-attachments/assets/766dbe56-4c3d-4e8b-ab70-80fbd32dadbf">











