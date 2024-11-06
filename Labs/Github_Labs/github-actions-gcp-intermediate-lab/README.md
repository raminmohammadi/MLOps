# CI/CD with GitHub Actions and GCP - Intermediate Lab

This repository is a hands-on lab designed to teach you how to set up a CI/CD pipeline for a machine learning project using GitHub Actions and Google Cloud Platform (GCP). You'll learn how to train a model, version it, and deploy it using Docker containers on GCP.

---
## Learning Objectives
By completing this lab, you will:
- Set up a GitHub repository with automated CI/CD using GitHub Actions for an ML project.
- Configure and use Google Cloud Platform (GCP) services for ML operations, including Google Cloud Storage (GCS) and Artifact Registry.
- Develop a GitHub Actions workflow that automates the entire process from testing to deploying a containerized ML model.
- Learn how to use MagicMock and patch for effectively testing functions that interact with GCP services.


---

### Step 1: Fork and Clone the Repository
First, you need to clone this repository onto your local machine. Then, Create a new repository in your GitHub account. Do not initialize it with a README, .gitignore, or license. Then you need to update the remote URL of your local repository to point to your new GitHub repository:

You can do so by the following command:
```bash
git remote set-url origin https://github.com/[your-username]/[your-new-repo-name].git
```
Now, push the cloned codes to new repository using below command:
```bash
git push -u origin main
```
Now you have a copy of the project in your own GitHub account. In the next steps, we'll set up the GCP project and configure the necessary credentials.

### Step 2: Setting up GCP and Configuring Credentials

1. Create a new project on GCP console.
2. Enable the following APIs in your GCP project: Cloud Storage, Cloud Build, Artifact Registry
3. Create a service account in your GCP project with the following roles:
- Storage Admin
- Storage Object Admin
- Artifact Registry Administrator

4. Generate a JSON key for the service account and download it.
5. Create a GCS bucket in your GCP project with a unique name. (we have done this step in the beginner lab, please refer to that one for more guidance)
6. In your GitHub repository, go to Settings > Secrets and variables > Actions.
7. Add the following repository secrets:
- `GCP_SA_KEY`: The entire content of the JSON key file you downloaded.
- `GCP_PROJECT_ID`: Your GCP project ID.
- `GCS_BUCKET_NAME`: The name of the GCS bucket you created in the previous step which we will use to store the model and version file.
- `VERSION_FILE_NAME`: The name of the file that will store the model version (e.g., "model_version.txt").


8. Create an Artifact Registry repository in your GCP project: You can either go to Artifact Registry service of GCP, and create a new repository through GCP UI, or you can do it through `gcloud` command. However, for doing through gcloud, you need to install Google SDK on your machine, and also authenticate your account, and also set the new created project as the active project. you can create the repository by the following command:
```bash
gcloud artifacts repositories create my-repo --repository-format=docker --location=us-east4
```

These steps set up your GCP environment and configure the necessary credentials for the GitHub Actions workflow to interact with GCP services.

### Step 3: Local Development Setup
For local development and testing the script, first we need to create a virtual environment by following commands:
```bash
# Creating a virtual environment
python -m venv venv

# Activating the environment
source venv/bin/activate

# Install required dependencies for this project
pip install -r requirements.txt
```
Now, we need to create `.env` file for storing environmental variables which will be used to load `GCS_BUCKET_NAME` and `VERSION_FILE_NAME` by the `dotenv` library in `train_and_save_model.py`.
```bash
# This is inside .env file
GCS_BUCKET_NAME=your-bucket-name
VERSION_FILE_NAME=model_version.txt
```

Replace your-bucket-name with the name of the GCS bucket you created earlier.

In order to interact with GCP services locally, we need to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the JSON key file:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

(Optional) If you want to use the gcloud CLI as well:

If you haven't already, install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install). After installing Google Cloud SDK, do the following commands:
 ```bash
 # Authenticate with your Google Cloud account
 gcloud auth application-default login

 # Set your project ID
 gcloud config set project your-project-id
 ```
 #### Running the Model Training Script
 To run the model training script locally:
 ```bash
 python train_and_save_model.py
 ```

 After running this script locally, there should be a `trained_models` and `model_version.txt` in your GCS bucket. If you run it one more time, the new model would be uploaded and also the model version increments by one.
 
This is a simple model script which we have also used in the previous beginner lab. This script includes following fucntions which will form our machine learning pipeline:
- Download the Iris dataset
- Preprocess the data
- Train a Random Forest model
- Evaluate the model's accuracy
- Save the model to your local machine and to Google Cloud Storage
- Update the model version in GCS

The train_and_save_model.py script contains several key functions:

- `download_data()`: Downloads the Iris dataset.
- `preprocess_data()`: Splits the data into training and testing sets.
- `train_model()`: Trains a Random Forest classifier.
- `get_model_version()`: Retrieves the current model version from GCS.
- `update_model_version()`: Updates the model version in GCS.
- `save_model_to_gcs()`: Saves the trained model to both the local filesystem and GCS.

The main() function orchestrates the entire process, from data download to model saving and version updating.

Review the code comments for more detailed explanations of each function.

### Step 4: GitHub Actions Workflow
This project includes a GitHub Actions workflow that automates the process of training the model, building a Docker image, and pushing it to Google Cloud Artifact Registry.

Key Steps in the Workflow: 

- Checkout code: Uses `actions/checkout@v4` to clone the repository.
- Set up Python: Uses `actions/setup-python@v5` to set up Python 3.10.
- Cache dependencies: Uses `actions/cache@v4` to cache pip dependencies.
- Install dependencies: Installs the required Python packages from requirements.txt.
- Run tests: Executes the test functions using pytest.
- Authenticate with GCP: Uses `google-github-actions/auth@v2` to authenticate with Google Cloud Platform using the service account key stored in GitHub Secrets.
- Set up Cloud SDK: Uses `google-github-actions/setup-gcloud@v1` to set up the Google Cloud SDK.
- Train and save model: Runs the `train_and_save_model.py` script, which trains the model and saves it to GCS. It also extracts the model version for use in later steps.
- Build and Push Docker image: Builds a Docker image containing the trained model and pushes it to Google Cloud Artifact Registry. The image is tagged with both the model version and 'latest'.

The Docker build and push process is a crucial part of the workflow. 
```yaml
- name: Build and Push Docker image
  env:
    IMAGE_NAME: ${{ env.REGION }}-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/${{ env.REPOSITORY_NAME }}/model-image
  run: |
    docker build -t ${IMAGE_NAME}:${{ env.MODEL_VERSION }} .
    docker push ${IMAGE_NAME}:${{ env.MODEL_VERSION }}
    docker tag ${IMAGE_NAME}:${{ env.MODEL_VERSION }} ${IMAGE_NAME}:latest
    docker push ${IMAGE_NAME}:latest
```
Here's what each command does:

- `docker build -t ${IMAGE_NAME}:${{ env.MODEL_VERSION }} .`

Builds a Docker image using the Dockerfile in the current directory (.).
Tags the image with the Artifact Registry repository path and the current model version (which is extracted using previous step using `grep` command).


- `docker push ${IMAGE_NAME}:${{ env.MODEL_VERSION }}`

Pushes the image with the version tag to the Artifact Registry.


- `docker tag ${IMAGE_NAME}:${{ env.MODEL_VERSION }} ${IMAGE_NAME}:latest`

Creates a new tag latest for the same image.
This allows users to always pull the most recent version using the latest tag.


- `docker push ${IMAGE_NAME}:latest`

Pushes the image with the latest tag to the Artifact Registry.



The `$IMAGE_NAME` environment variable is constructed using:

- `${{ env.REGION }}`: The GCP region (us-east4)
- `${{ secrets.GCP_PROJECT_ID }}`: Your GCP project ID (stored in GitHub Secrets)
- `${{ env.REPOSITORY_NAME }}`: The Artifact Registry repository name (`my-repo`)


This process ensures that each model version is uniquely tagged and pushed to the Artifact Registry, while also maintaining a latest tag that always points to the most recent version.

### Step 3: Monitor the GitHub Actions Workflow
If you've made any changes to the code or configuration files, commit them to your local repository and push to GitHub:
```bash
git add .
git commit -m "Completed MLOps Intermediate Lab setup"
git push origin main
```
If you haven't made any changes, then you can create an empty commit by the following command and push it to the remote repo to trigger the workflow:
```bash
git commit --allow-empty -m "Trigger the pipeline by an empty commit"

git push
```
Once the workflow completes successfully, verify the results in your Google Cloud Console by going to Artifact Registry and look for `my-repo` repository. You should see your Docker image with two tags, 

a specific version number (e.g., `1, 2, 3`, etc.) and the `latest` tag.