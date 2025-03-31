[![pages-build-deployment](https://github.com/raminmohammadi/MLOps/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/raminmohammadi/MLOps/actions/workflows/pages/pages-build-deployment)

# IE 7305 - MLOps

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

- [API_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/API_Labs)
  - [FastAPI_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/API_Labs/FastAPI_Labs)
  - [Streamlit_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/API_Labs/Streamlit_Labs)
- [Airflow_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Airflow_Labs)
  - [Lab_1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_1)
  - [Lab_2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_2)
  - [Lab_3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_3)
- [Data_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Data_Labs)
  - [Apache_Beam_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Data_Labs/Apache_Beam_Labs)
  - [DVC_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Data_Labs/DVC_Labs)
    - [Lab_1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_1)
  - [Data_Labeling_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Data_Labs/Data_Labeling_Labs)
- [Docker_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Docker_Labs)
  - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
  - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
- [ELK_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/ELK_Labs)
  - [Lab1_Setup_Windows_WSL_Ubuntu](https://github.com/raminmohammadi/MLOps/tree/main/Labs/ELK_Labs/Lab1_Setup_Windows_WSL_Ubuntu)
  - [Lab2_ELK_Setup_Mac](https://github.com/raminmohammadi/MLOps/tree/main/Labs/ELK_Labs/Lab2_ELK_Setup_Mac)
  - [Lab3_Example](https://github.com/raminmohammadi/MLOps/tree/main/Labs/ELK_Labs/Lab3_Example)
- [Experiment_Tracking_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Experiment_Tracking_Labs)
  - [Logging_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Experiment_Tracking_Labs/Logging_Labs)
  - [Mlflow_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Experiment_Tracking_Labs/Mlflow_Labs)
    - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
    - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
- [GCP_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs)
  - [CloudFunction_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/CloudFunction_Labs)
    - [CloudFunction_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/CloudFunction_Labs)
      - [Lab-3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/CloudFunction_Labs/CloudFunction_Labs/Lab-3)
    - [Lab1-CloudFunction_Setup](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/CloudFunction_Labs/Lab1-CloudFunction_Setup)
    - [Lab2 - CloudFunction_Intermediate](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/CloudFunction_Labs/Lab2 - CloudFunction_Intermediate)
  - [Cloud_Composer_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Cloud_Composer_Labs)
    - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
    - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
    - [Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab3)
  - [Cloud_Runner_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Cloud_Runner_Labs)
    - [Begineer_Lab](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Cloud_Runner_Labs/Begineer_Lab)
    - [Intermediate_Lab](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Cloud_Runner_Labs/Intermediate_Lab)
  - [Compute_Engine_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Compute_Engine_Labs)
    - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
    - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
    - [Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab3)
  - [Data_Storage_Warehouse_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Data_Storage_Warehouse_Labs)
    - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
    - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
    - [Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab3)
  - [KServe_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/KServe_Labs)
    - [Lab 1 - Introduction to KServer and K8s](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/KServe_Labs/Lab 1 - Introduction to KServer and K8s)
    - [Lab 2 - Installing KServe on K8s cluster](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/KServe_Labs/Lab 2 - Installing KServe on K8s cluster)
    - [Lab 3 - Deployment of first model](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/KServe_Labs/Lab 3 - Deployment of first model)
    - [Lab 4 - KServer HPA and Metrics](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/KServe_Labs/Lab 4 - KServer HPA and Metrics)
  - [Kubeflow_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubeflow_Labs)
    - [Lab1-Kubeflow_Setup](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubeflow_Labs/Lab1-Kubeflow_Setup)
    - [Lab2-Kubeflow_Katlib](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubeflow_Labs/Lab2-Kubeflow_Katlib)
    - [Lab3-Advanced_Lab](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubeflow_Labs/Lab3-Advanced_Lab)
  - [Kubernetes_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs)
    - [Lab 1-Creating GKE Cluster](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab 1-Creating GKE Cluster)
    - [Lab 2-Deploying App on GKE](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab 2-Deploying App on GKE)
    - [Lab 3-Application Scaling](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab 3-Application Scaling)
    - [Lab 4-Deployment Strategies](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab 4-Deployment Strategies)
    - [Lab 5-Configuring Networking](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab 5-Configuring Networking)
    - [Lab_Class_Demo](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Kubernetes/Kubernetes_Labs/Lab_Class_Demo)
  - [Lab-2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab-2)
  - [Lab_1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_1)
  - [Lab_2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_2)
  - [Lab_3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/GCP_Labs/Vertex_AI/Lab_3)
- [Github_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs)
  - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
  - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
  - [Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab3)
  - [Lab4](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Github_Labs/Lab4)
- [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
- [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
- [MLMD_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/MLMD_Labs)
  - [Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab1)
  - [Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Model_Development/Distributed_Training/Lab2)
- [Tensorflow_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs)
  - [TFDV_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFDV_Labs)
    - [TFDV_Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFDV_Labs/TFDV_Lab1)
    - [TFDV_Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFDV_Labs/TFDV_Lab2)
    - [TFDV_Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFDV_Labs/TFDV_Lab3)
  - [TFT_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFT_Labs)
  - [TFX_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFX_Labs)
    - [TFX_Lab1](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFX_Labs/TFX_Lab1)
    - [TFX_Lab2](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFX_Labs/TFX_Lab2)
    - [TFX_Lab3](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Tensorflow_Labs/TFX_Labs/TFX_Lab3)
- [Terraform_Labs](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Terraform_Labs)
  - [Lab1_Beginner](https://github.com/raminmohammadi/MLOps/tree/main/Labs/Terraform_Labs/GCP/Lab1_Beginner)

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

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=raminmohammadi/MLOps&type=Date)](https://star-history.com/#raminmohammadi/MLOps&Date)

## Contributors
[![MLOPs contributors](https://contrib.rocks/image?repo=raminmohammadi/MLOps)](https://github.com/raminmohammadi/MLOps/graphs/contributors)
