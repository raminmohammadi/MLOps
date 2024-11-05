[![pages-build-deployment](https://github.com/raminmohammadi/MLOps/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/raminmohammadi/MLOps/actions/workflows/pages/pages-build-deployment)

# MLOps Repository 

## Overview

Welcome to the MLOps Repository! This repository is dedicated to sharing reading contents, labs and exercises for the MLOps (Machine Learning Operations) course at Northeastern University. The primary goal of this repository is to provide a centralized platform for students, instructors, and anyone interested in MLOps to access and collaborate on course-related materials. You can learn more on Machine learning topics by watching my videos on [Youtube](https://www.youtube.com/channel/UCCGbsdfmgmhMLs-tjOtOp0Q) or visit my [Website](https://www.mlwithramin.com/).

## Table of Contents

- [Introduction](#introduction)
- [Course Description](#course-description)
- [Lab Content](#lab-content)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Introduction

MLOps is an emerging discipline that focuses on the collaboration and communication of both data scientists and IT professionals while automating and streamlining the machine learning lifecycle. It bridges the gap between machine learning development and production deployment, ensuring that machine learning models are scalable, reproducible, and maintainable. This repository serves as a resource hub for students and instructors of Northeastern University's MLOps course.

## Course Description

The MLOps course at Northeastern University is designed to provide students with a comprehensive understanding of the MLOps field. Throughout the course, students will learn how to:

- Build end-to-end machine learning pipelines
- Deploy machine learning models to production
- Monitor and maintain ML systems
- Implement CI/CD/CM/CT (Continuous Integration/Continuous Deployment/Continuous Monitoring/Continuous Training) for ML
- Containerize and orchestrate ML workloads
- Handle data drift and model retraining

This repository hosts the labs, code samples, and documentation related to these topics.

## Labs Content

This repository offers a series of hands-on labs designed to enhance your understanding of MLOps concepts. Each lab focuses on a specific aspect of the machine learning lifecycle, providing practical experience with tools and methodologies essential for deploying and managing machine learning models in production environments.

1. **[API Labs](./Labs/API_Labs)**
   - **Objective:** Learn to develop and deploy APIs for ML models.
   - **Sub-Labs:**
     - **[FLASK_GCP_LAB](./Labs/API_Labs/FLASK_GCP_LAB):** Flask lab data.
     - **[FastAPI Labs](./Labs/API_Labs/FastAPI_Labs):** FastAPI lab details.
     - **[Streamlit Labs](./Labs/API_Labs/Streamlit_Labs):** Streamlit README - updated.

2. **[Airflow Labs](./Labs/Airflow_Labs)**
   - **Objective:** Gain practical experience with Apache Airflow for orchestrating complex data workflows.
   - **Sub-Labs:**
     - **[Lab 1](./Labs/Airflow_Labs/Lab_1):** Basic Airflow setup and DAGs.
     - **[Lab 2](./Labs/Airflow_Labs/Lab_2):** Advanced DAG dependencies and scheduling.
     - **[assets](./Labs/Airflow_Labs/assets):** Contains additional assets for Airflow labs.

3. **[CloudFunction Labs](./Labs/CloudFunction_Labs)**
   - **Objective:** Learn how to deploy lightweight functions using cloud-based services.
   - **Sub-Labs:**
     - **[Lab1-CloudFunction Setup](./Labs/CloudFunction_Labs/Lab1-CloudFunction_Setup):** Setting up Google Cloud Functions.
     - **[Lab2-CloudFunction Intermediate](./Labs/CloudFunction_Labs/Lab2-CloudFunction_Intermediate):** Intermediate Cloud Function concepts and use cases.

4. **[Data Labs](./Labs/Data_Labs)**
   - **Objective:** Understand data engineering and preprocessing steps.
   - **Sub-Labs:**
     - **[Apache](./Labs/Data_Labs/Apache):** Apache setup for data handling.
     - **[DVC Labs/Lab 1](./Labs/Data_Labs/DVC_Labs/Lab_1):** DVC setup and basic commands.
     - **[Data Labeling Labs](./Labs/Data_Labs/Data_Labeling_Labs):** Lab focused on data labeling processes.

5. **[Data Storage & Warehouse Labs](./Labs/Data_Storage_Warehouse_Labs)**
   - **Objective:** Explore data storage solutions and data warehousing.
   - **Sub-Labs:**
     - **[Lab1](./Labs/Data_Storage_Warehouse_Labs/Lab1):** Introduction to data warehousing.
     - **[Lab2](./Labs/Data_Storage_Warehouse_Labs/Lab2):** Advanced data storage techniques.
     - **[Lab3](./Labs/Data_Storage_Warehouse_Labs/Lab3):** Optimization and data retrieval practices.

6. **[Docker Container Labs](./Labs/Docker_Container_Labs)**
   - **Objective:** Learn containerization techniques for ML applications.
   - **Sub-Labs:**
     - **[Week7_Docker_Container](./Labs/Docker_Container_Labs/Week7_Docker_Container):** Introduction to Docker containers.
     - **[Week8_Docker_Container](./Labs/Docker_Container_Labs/Week8_Docker_Container):** Advanced Docker techniques and orchestration.

7. **[ELK Labs](./Labs/ELK_Labs)**
   - **Objective:** Set up logging and monitoring using the ELK stack.
   - **Sub-Labs:**
     - **[Lab1_Setup_Windows_WSL_Ubuntu](./Labs/ELK_Labs/Lab1_Setup_Windows_WSL_Ubuntu):** ELK setup on Windows with WSL.
     - **[Lab2_ELK_Setup_Mac](./Labs/ELK_Labs/Lab2_ELK_Setup_Mac):** ELK setup on macOS.
     - **[Lab3_Example](./Labs/ELK_Labs/Lab3_Example):** Example of ELK in practice.

8. **[Experiment Tracking Labs](./Labs/Experiment_Tracking_Labs)**
   - **Objective:** Track and manage ML experiments.
   - **Sub-Labs:**
     - **[Logging Labs](./Labs/Experiment_Tracking_Labs/Logging_Labs):** Tracking logs for model training.
     - **[Mlflow Labs](./Labs/Experiment_Tracking_Labs/Mlflow_Labs):** Using MLflow for experiment tracking.

9. **GCP Labs**
   - **[Cloud Composer Labs](./Labs/GCP_Labs/Cloud_Composer_Labs):** Set up and manage workflows with Cloud Composer.
   - **[Compute Engine Labs](./Labs/GCP_Labs/Compute_Engine_Labs):** Hands-on with Google Compute Engine.
   - **[KServe Labs](./Labs/GCP_Labs/KServe_Labs):** Serving ML models with KServe on Kubernetes.
   - **[Kubernetes Labs](./Labs/GCP_Labs/Kubernetes_Labs):** Running and managing containers on GKE.
   - **[Vertex AI Labs](./Labs/GCP_Labs/Vertex_AI):** End-to-end ML workflows with Vertex AI.

10. **[GitHub Labs](./Labs/Github_Labs)**
    - **Objective:** Implement GitHub Actions for CI/CD.
    - **Sub-Labs:**
      - **[GitHub_Actions_GCP_Lab_beginner](./Labs/Github_Labs/GitHub_Actions_GCP_Lab_beginner):** Beginner-level CI/CD with GitHub Actions.
      - **[Lab1](./Labs/Github_Labs/Lab1):** Basics of GitHub Actions.
      - **[Lab2](./Labs/Github_Labs/Lab2):** Intermediate CI/CD practices with GitHub.
      - **[github-actions-gcp-intermediate-lab](./Labs/Github_Labs/github-actions-gcp-intermediate-lab):** Intermediate GCP integration with GitHub Actions.

11. **[Kubeflow Labs](./Labs/Kubeflow_Labs)**
    - **Objective:** Orchestrate ML workflows with Kubeflow.
    - **Sub-Labs:**
      - **[Lab1-Kubeflow Setup](./Labs/Kubeflow_Labs/Lab1-Kubeflow_Setup):** Setting up Kubeflow environment.
      - **[Lab2-Kubeflow Katib](./Labs/Kubeflow_Labs/Lab2-Kubeflow_Katib):** Hyperparameter tuning with Katib in Kubeflow.

12. **[MLMD Labs](./Labs/MLMD_Labs)**
    - **Objective:** Understand ML Metadata (MLMD) for tracking metadata.
    - **Sub-Labs:**
      - **[Lab1](./Labs/MLMD_Labs/Lab1):** Introduction to ML metadata concepts.
      - **[Lab2](./Labs/MLMD_Labs/Lab2):** Advanced usage and querying of ML metadata.
      - **[assets](./Labs/MLMD_Labs/assets):** Supporting materials and assets for MLMD labs.

13. **[TensorFlow Labs](./Labs/Tensorflow_Labs)**
    - **Objective:** Gain hands-on experience with TensorFlow for ML model development.
    - **Sub-Labs:**
      - **[TFDV Labs](./Labs/Tensorflow_Labs/TFDV_Labs):** TensorFlow Data Validation labs.
      - **[TFDV TFX Installation](./Labs/Tensorflow_Labs/TFDV_TFX_Installation):** Setting up TFX and TFDV.
      - **[TFT Labs](./Labs/Tensorflow_Labs/TFT_Labs):** TensorFlow Transform labs.
      - **[TFX Labs](./Labs/Tensorflow_Labs/TFX_Labs):** TensorFlow Extended for production pipelines.

Each lab is accompanied by detailed instructions and code examples to facilitate hands-on learning. It's recommended to follow the labs sequentially, as concepts build upon each other. For additional resources and support, refer to the [Reading Materials](./Labs/Reading%20Materials) section of this repository.


## Getting Started

To get started with the labs and exercises in this repository, please follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the specific lab you are interested in.
3. Read the lab instructions and review any accompanying documentation.
4. Follow the provided code samples and examples to complete the lab exercises.
5. Feel free to explore, modify, and experiment with the code to deepen your understanding.

For more detailed information on each lab and prerequisites, please refer to the lab's README or documentation.

## Contributing

Contributions to this repository are welcome! If you are a student or instructor and would like to contribute your own labs, improvements, or corrections, please follow these guidelines:

1. Fork this repository.
2. Create a branch for your changes.
3. Make your changes and commit them with clear, concise messages.
4. Test your changes to ensure they work as expected.
5. Submit a pull request to the main repository.

Your contributions will help improve the overall quality of the labs and benefit the entire MLOps community.

## Reference:
The reading materials of this repo was collected from Coursera under the Creative Commons License.

## License

This repository is open-source and is distributed under the [Creative Commons License](LICENSE). Please review the license for more details on how you can use and share the content within this repository.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=raminmohammadi/MLOps&type=Date)](https://star-history.com/#raminmohammadi/MLOps&Date)

## 🌟 Contributors
[![MLOPs contributors](https://contrib.rocks/image?repo=raminmohammadi/MLOps)](https://github.com/raminmohammadi/MLOps/graphs/contributors)
