# Pipelines with AutoML and Pre-built Containers
In this lab, we'll explore how to create end-to-end pipelines and get online predictions in Vertex AI using AutoML.
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
### Prediction
The GCP interface has this feature where you can test if the deployed model on endpoint is working or not by giving the inputs without having to run the " curl  -POST " command directly in the same "DELPOY & TEST" page
<img width="1507" alt="Screenshot 2024-10-05 at 12 27 13 AM" src="https://github.com/user-attachments/assets/0cfe63ed-15eb-4cba-a6b0-28421946389e">
Now if you run the commands shown in `SAMPLE REQUEST` you'll get a URL similar to 
`https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict`
Now to actually send data to this model and get predictions, you can copy and paste this link into POSTMAN application.
To run this you'll need an access token to your GCP, which you'll get by running this command `gcloud auth print-access-token`
in Google cloud shell
Use this token as authorization in the POSTMAN application and give your data in the format specified in the `SAMPLE REQUEST` to get your prediction.
<img width="1497" alt="Screenshot 2024-10-05 at 12 54 12 AM" src="https://github.com/user-attachments/assets/766dbe56-4c3d-4e8b-ab70-80fbd32dadbf">
While AutoML is hassle-free, it abstracts most machine learning pipelines, including model selection, hyperparameter tuning, and feature engineering. While this is beneficial for users with less ML expertise, it provides less control for advanced users who might want to experiment with custom algorithms or fine-tune specific parameter and is very costly to train.
## End-to-end pipeline with custom model and pre-built container
Pre-built Containers provide more flexibility and are generally better suited for highly specialized use cases, large-scale custom models, or where specific optimization is needed.
In this method, we'll use our own machine-learning model with pre-built containers like TensorFlow, Scikit-learn, Pytorch & XGBoost
which covers most of the use cases.
For this, we'll use a different dataset https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
**Application structure**
stroke_package
--setup.py
  trainer
  --__init__.py
  --task.py
 ### Source Distribution 
Before you can perform custom training with a prebuilt container, you must create a [Python source distribution](https://cloud.google.com/vertex-ai/docs/training/create-python-pre-built-container.com) that contains your training application and upload it to a Cloud Storage bucket that your Google Cloud project can access. 
Create this kind of structure with the files in the repository in your GCP workbench (jupyterlab) and open a terminal inside that jupyter lab
`python setup.py sdist --formats=gztar`
This command creates required source distribution
you'll see 2 new folders `dist` & `trainer.egg-info` as shown below
<img width="1433" alt="Screenshot 2024-10-05 at 2 34 33 AM" src="https://github.com/user-attachments/assets/b15670b4-04b9-4f21-a4b4-4f0bb160096b">
now upload this source distribution to cloud storage using the command
`gcloud storage cp dist/trainer-0.1.tar.gz gs://vertexai-lab2/prebuilt_container`
<img width="1496" alt="Screenshot 2024-10-05 at 2 37 58 AM" src="https://github.com/user-attachments/assets/a9460f15-52c4-43cf-b116-45fdba6058f1">
###Training Model
Now we'll start a new training job with `No managed dataset`
<img width="1506" alt="Screenshot 2024-10-05 at 2 44 29 AM" src="https://github.com/user-attachments/assets/b470c3ed-4a66-4d38-ac3d-8e57bd9aff79">
Now I'm naming the new training job "stroke_model" and leave the rest as default
<img width="1498" alt="Screenshot 2024-10-05 at 2 45 56 AM" src="https://github.com/user-attachments/assets/586ef663-5c84-4f60-8df8-3aab3c50774d">
Before we go to next step make sure to create 2 new buckets in GCS (google cloud storage) for "model_outputs" and to store the "dataset" 
- Now click the  `pre-built container`
- choose framework `scikit-learn` and version `0.23`
- now for `Package location (cloud storage path) 1` choose the cloud directory where you uploaded the source distribution "gs://vertexai-lab2/prebuilt_container"
- python module is your training code, here it is `trainer.task` (path to task.py in trainer folder as in the initial structure)
- Model output directory is  "gs://stroke_outputs/job_outputs/model/"
- At last, give your data location as argument in the "Arguments" section 
  " --data_gcs_path= gs://stroke_dataset_test/stroke_data.csv " (in task.py we wrote the code to take in a argument of data location )
  
<img width="1512" alt="Screenshot 2024-10-05 at 2 55 39 AM" src="https://github.com/user-attachments/assets/4e4c298e-d0d6-49cb-b358-dd96a8bbd26a">
<img width="610" alt="Screenshot 2024-10-05 at 2 55 45 AM" src="https://github.com/user-attachments/assets/2c84ee0f-cf89-4792-ad0b-23c05e7ddff1">
Now you can select hyperparameters as per the model requirements and select the required compute resources for training and click continue
Wait for the training job to get finished then you'll see something of this sort
<img width="1487" alt="Screenshot 2024-10-05 at 3 37 17 AM" src="https://github.com/user-attachments/assets/a556447f-b5a6-4561-a8a6-6f6bf5700536">
Now after the training, you'll see the "model.joblib" file saved for further usage in GCS model output bucket given while initiating training job
<img width="1502" alt="Screenshot 2024-10-05 at 3 41 58 AM" src="https://github.com/user-attachments/assets/b08e53ea-628f-46f6-9ce2-3801e4e149a3">
Now open `Model Registry` in GCP console and select the import button
- Now name the model and give the region you're located in
- For "model settings" select the model framework, version and give the location of the Model artifact location "gs://stroke_outputs/job_outputs/model/model.joblib"
- leave rest as default settings
<img width="1478" alt="Screenshot 2024-10-05 at 3 56 27 AM" src="https://github.com/user-attachments/assets/e046a510-1d99-4abd-a59b-1d4dc261e71c">
Now you can see the model in the model registry, we have to next deploy the model to an endpoint, follow a similar path as mentioned in AutoML method and you can see the predictions

<img width="1512" alt="Screenshot 2024-10-05 at 4 13 22 AM" src="https://github.com/user-attachments/assets/199f41c0-7fde-41b8-be66-2db271a109c7">

NOTE: Important points

**NOTE: Important points**

- INPUT_DATA_FILE should be a .json file
- Also you should make sure that no.of input features for your model in the training script should match the input you're giving to the model deployed at the endpoint


