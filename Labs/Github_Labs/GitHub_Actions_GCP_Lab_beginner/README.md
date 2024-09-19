# GitHub Actions and GCP Connections: Beginner Lab

## Overview
Welcome to the "GitHub Actions and GCP Connections" beginner lab! In this lab, you will learn how to automate a machine learning workflow using GitHub Actions and Google Cloud Platform (GCP). By the end of the lab, you will understand how to connect GitHub Actions to GCP, allowing you to automate the process of training a machine learning model and uploading the results to Google Cloud Storage (GCS).

The provided project includes a simple machine learning model (RandomForestClassifier) trained on the Iris dataset. Your focus will be on setting up the cloud environment and automating the workflow using GitHub Actions.

## Learning Objectives
By completing this lab, you will:

1. Learn how to set up a GCP project and configure a service account for automation.
2. Understand how to grant GitHub Actions access to your GCP project.
3. Automate the process of training and saving a model using GitHub Actions.
4. Use Google Cloud Storage (GCS) to store your trained machine learning model.

## Setup

### Step 1: Create a New GitHub Repository
1. Go to GitHub and create a new repository. Name it something like `gh-actions-gcp-beginner-lab`.
2. Don't initialize the repository with a README or .gitignore.
3. Note the URL of your new repository.

### Step 2: Clone the Template Repository and Set Up Your Project
Instead of cloning the original repository directly, we'll clone it, then push it to your new repository:

```bash
# Clone the template repository
git clone https://github.com/AshyScripts/github-actions-gcp-beginner-lab.git

# Navigate into the new directory
cd github-actions-gcp-beginner-lab

# Remove the existing Git configuration
rm -rf .git

# Initialize a new Git repository
git init

# Add all files to the new repository
git add .

# Commit the files
git commit -m "Initial commit"

# Set the remote to your new GitHub repository
git remote add origin https://github.com/your-username/gh-actions-gcp-beginner-lab.git

# Push the code to your new repository
git push -u origin main
```

Replace `your-username` with your actual GitHub username in the remote URL.

### Step 3: Create a Virtual Environment and Install Dependencies
To follow along this lab, you need to install required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Step 4: Set Up Google Cloud Platform (GCP)
1. Create a New GCP Project in Google Cloud Console. 
2. Create a service account and give it the required roles and permissions to interact with Google Cloud Storage. Go to `IAM & Admin` section and add the `Storage Admin` role.
3. Generate a JSON key for the service account. Save it securely.

### Step 5: Create a Google Cloud Storage (GCS) Bucket
1. Go to Google Cloud Console
2. Navigate to the Storage section, and select Buckets
3. Create a new bucket. Choose a unique name for your bucket.
4. Note the bucket name for use in the `train_and_save_model.py` script and the GitHub Actions workflow.

### Step 6: Upload the Service Account JSON Key to GitHub Actions Secrets
1. Go to your GitHub repository's Settings.
2. Navigate to Secrets and variables > Actions > New repository secret.
3. Name the secret `GCP_SA_KEY`.
4. Paste the entire contents of the service account JSON key file into the secret value field and click Add secret.

### Step 7: Set Up GitHub Actions Workflow
Now that you’ve added the JSON key, we can set up the GitHub Actions workflow to automate the model training and uploading process.

1. In the root directory of the project, there should be a folder named `.github` and in this folder, there should be another folder (nested) named `workflows`. This is where GitHub Actions read different workflow `yaml` files. 

2. For the current project, there should be a file in `.github/workflows` named `train-and-upload.yml`. If not, create a file with this name and this file should have below content:

```yaml
name: Train and save model to GCS

on:
  schedule:
    - cron: '0 0 * * *' # Run every day at midnight
  workflow_dispatch: # Run manually

jobs:
  train_and_save:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout the code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Get cache dir 
        id: pip-cache-dir
        run: echo "dir=$(pip cache dir)" >> $GITHUB_OUTPUT
      
      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ${{ steps.pip-cache-dir.outputs.dir}}
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Authenticate with GCP
        uses: 'google-github-actions/auth@v2'
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY }}'

      - name: Train and save model
        run: |
          python train_and_save_model.py
```
 In this workflow we are instructing GitHub Actions to do below step by defining `train_and_save` job:
 
 - Workflow is scheduled to run each day at midnight using cron expressions.
 - Then we check out the code (`actions/checkout@v4`), and then we set up a Python environment (`actions/setup-python@v5`) with version `3.10` to run the necessary scripts.
 - We get the directory where `pip` caches installed dependencies. 
- Cache pip dependencies: this is a useful step which caches pip dependencies based on the `requirements.txt`. `key` parameter is set to be based on the `runner.os` and also we use `hashFiles('**/requirements.txt')` to generate a unique number based on the requiremenets. So, if in the future runs, requirements is updated, GitHub Actions will install the new dependencies. 
- Authenticate with GCP: This step authenticates the GitHub Actions runner with Google Cloud using the service account key stored in the GitHub repository secrets as `GCP_SA_KEY`. This authentication allows the workflow to interact with Google Cloud resources, such as Google Cloud Storage (GCS).
