# Using GitHub Actions for Model Training and Versioning

This repository demonstrates how to use GitHub Actions to automate the process of training a machine learning model, storing the model, and versioning it. This allows you to easily update and improve your model in a collaborative environment.

## Prerequisites

- [GitHub](https://github.com) account
- Basic knowledge of Python and machine learning
- Git command-line tool (optional)

## Getting Started

1. **Fork this Repository**: Click the "Fork" button at the top right of this repository to create your own copy.

2. **Clone Your Repository**:
   ```bash
   git clone https://github.com/your-username/your-forked-repo.git
   cd your-forked-repo

   ```
3. GitHub account
4. Basic knowledge of Python and machine learning
5. Git command-line tool (optional)


# Getting Started

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```
2. **Create a GitHub Personal Access Token (PAT):**
- Go to your GitHub Developer Settings.
- Generate a new token with the repo scope.
- Save this token in a safe place.

3. **Add the PAT as a Repository Secret:**
- In your forked repository, go to Settings > Secrets.
- Add a new secret named GITHUB_TOKEN and paste your PAT as the value.

   
# Running the Workflow

## Customize Model Training
1. Modify the `train_model.py` script in the `src/` directory according to your dataset and model requirements. This script generates synthetic data for demonstration purposes.

## Push Your Changes
1. Commit your changes and push them to your forked repository.

## GitHub Actions Workflow
1. Once you push changes to the main branch, the GitHub Actions workflow will be triggered automatically.

## View Workflow Progress
1. You can track the progress of the workflow by going to the "Actions" tab in your GitHub repository.

## Retrieve the Trained Model
1. After the workflow completes successfully, the trained model will be stored in the `models/` directory.

# Model Evaluation
The model evaluation is performed automatically within the GitHub Actions workflow. The evaluation results (e.g., F1 Score) are stored in the `metrics/` directory.

# Versioning the Model
Each time you run the workflow, a new version of the model is created and stored. You can access and use these models for your projects.

# GitHub Actions Workflow Details
The workflow consists of the following steps:

- Generate and Store Timestamp: A timestamp is generated and stored in a file for versioning.
- Model Training: The `train_model.py` script is executed, which trains a random forest classifier on synthetic data and stores the model in the `models/` directory.
- Model Evaluation: The `evaluate_model.py` script is executed to evaluate the model's F1 Score on synthetic data, and the results are stored in the `metrics/` directory.
- Store and Version the New Model: The trained model is moved to the `models/` directory with a timestamp-based version.
- Commit and Push Changes: The metrics and updated model are committed to the repository, allowing you to track changes.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
- This project uses GitHub Actions for continuous integration and deployment.
- Model training and evaluation are powered by Python and scikit-learn.

# Questions or Issues
If you have any questions or encounter issues while using this GitHub Actions workflow, please open an issue in the Issues section of your repository.

