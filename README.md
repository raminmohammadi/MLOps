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
   - **Key Topics:**
     - Flask and FastAPI basics
     - Building and serving prediction APIs

2. **[Airflow Labs](./Labs/Airflow_Labs)**
   - **Objective:** Gain practical experience with Apache Airflow for orchestrating complex data workflows.
   - **Key Topics:**
     - DAG creation and scheduling
     - Task dependencies and monitoring

3. **[CloudFunction Labs](./Labs/CloudFunction_Labs)**
   - **Objective:** Learn how to deploy lightweight functions using cloud-based services.
   - **Key Topics:**
     - Cloud Function basics
     - Event-driven programming

4. **[Data Labs](./Labs/Data_Labs)**
   - **Objective:** Understand data engineering and preprocessing steps.
   - **Key Topics:**
     - Data cleaning and transformation
     - Data pipeline setup

5. **[Data Storage & Warehouse Labs](./Labs/Data_Storage_Warehouse_Labs)**
   - **Objective:** Explore data storage solutions and data warehousing.
   - **Key Topics:**
     - Data warehousing concepts
     - Storage optimization and management

6. **[Docker Container Labs](./Labs/Docker_Container_Labs)**
   - **Objective:** Learn containerization techniques for ML applications.
   - **Key Topics:**
     - Docker basics
     - Creating and managing containers

7. **[ELK Labs](./Labs/ELK_Labs)**
   - **Objective:** Set up logging and monitoring using the ELK stack.
   - **Key Topics:**
     - Elasticsearch, Logstash, and Kibana integration
     - Monitoring data pipelines

8. **[Experiment Tracking Labs](./Labs/Experiment_Tracking_Labs)**
   - **Objective:** Track and manage ML experiments.
   - **Key Topics:**
     - Logging metrics and parameters
     - Versioning experiments

9. **GCP Labs**
   - **[Cloud Composer Labs](./Labs/GCP_Labs/Cloud_Composer_Labs)**
     - **Objective:** Learn how to use Google Cloud Composer for managing and orchestrating workflows.
     - **Key Topics:**
       - Airflow integration in GCP
       - Workflow automation and scheduling

   - **[Compute Engine Labs](./Labs/GCP_Labs/Compute_Engine_Labs)**
     - **Objective:** Gain hands-on experience with Google Compute Engine for scalable virtual machine instances.
     - **Key Topics:**
       - Setting up and managing VMs
       - Using Compute Engine for ML model training

   - **[KServe Labs](./Labs/GCP_Labs/KServe_Labs)**
     - **Objective:** Explore KServe for serving ML models at scale on Kubernetes.
     - **Key Topics:**
       - Model serving with KServe
       - Scaling models on Kubernetes

   - **[Kubernetes Labs](./Labs/GCP_Labs/Kubernetes_Labs)**
     - **Objective:** Learn Kubernetes basics and deploy ML workloads in a managed Kubernetes environment.
     - **Key Topics:**
       - GKE setup and management
       - Deploying containers for ML

   - **[Vertex AI Labs](./Labs/GCP_Labs/Vertex_AI)**
     - **Objective:** Understand and utilize Vertex AI for end-to-end ML workflows.
     - **Key Topics:**
       - Managed datasets, training, and deployment
       - Model monitoring and pipeline automation

10. **[GitHub Labs](./Labs/Github_Labs)**
    - **Objective:** Implement GitHub Actions for CI/CD.
    - **Key Topics:**
      - Setting up workflows
      - Automating testing and deployment

11. **[Kubeflow Labs](./Labs/Kubeflow_Labs)**
    - **Objective:** Orchestrate ML workflows with Kubeflow.
    - **Key Topics:**
      - Kubeflow Pipelines
      - Model management

12. **[MLMD Labs](./Labs/MLMD_Labs)**
    - **Objective:** Understand ML Metadata (MLMD) for tracking metadata.
    - **Key Topics:**
      - Metadata storage and querying
      - Workflow lineage tracking

13. **[TensorFlow Labs](./Labs/Tensorflow_Labs)**
    - **Objective:** Gain hands-on experience with TensorFlow for ML model development.
    - **Key Topics:**
      - Model training and evaluation
      - Using TFX for production-grade ML pipelines

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
