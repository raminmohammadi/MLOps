# **Introduction to KServe and Kubernetes**

## KServe and Kubernetes

This ReadMe will walk you through the basics of **KServe**, its integration with **Kubernetes**, and how to set up a Kubernetes cluster using **Google Cloud Platform (GCP)**. By the end of this guide, you will have a better understanding of these technologies, including how to install and use them.

### **What is Kubernetes?**
Kubernetes (K8s) is an open-source platform that automates the deployment, scaling, and management of containerized applications. Containers bundle applications and all their dependencies into isolated environments, ensuring they run consistently across different computing environments.

Kubernetes provides:
- **Automatic scaling:** It can automatically adjust the number of running container instances based on demand.
- **Self-healing:** It restarts or replaces containers that fail.
- **Load balancing:** It ensures network traffic is distributed across all instances of a service.
- **Service discovery and networking:** It assigns containers unique IP addresses and a DNS name, simplifying how applications communicate within the cluster.

### **What is KServe?**
**KServe** is an open-source platform that simplifies deploying and serving machine learning models in production on Kubernetes. It supports models trained with popular frameworks like **TensorFlow**, **PyTorch**, and **Scikit-learn**. KServe manages the entire model lifecycle, from deployment and versioning to scaling and routing traffic.

## **Overview of KServe**
![](assets/kserver_main.png)

KServe helps data scientists and engineers by simplifying the deployment and serving of machine learning models, making the process much more efficient. You don’t need to worry about manually handling scaling, monitoring, or traffic routing—KServe handles it for you.

Here are some key features of KServe:
- **Standardized model interface:** It provides a unified way to serve models from different machine learning frameworks.
- **Autoscaling:** KServe can automatically scale up or down based on the traffic load.
- **Model versioning:** You can manage multiple versions of the same model and route a portion of traffic to different versions.
- **Traffic splitting:** KServe allows for a controlled rollout of models by directing traffic between different versions (canary releases).
- **Integration with Knative and Istio:** These tools provide KServe with scaling, networking, and routing capabilities.

### **Model Lifecycle in KServe**
KServe manages the entire lifecycle of model serving, which includes:
- **Model Deployment:** Once your model is trained, KServe simplifies the process of deploying it on Kubernetes.
- **Scaling:** Based on the traffic or demand, KServe automatically adjusts the number of running containers for your model.
- **Traffic Routing:** It intelligently routes requests to different versions of your model, allowing you to test and roll out new versions.
- **Monitoring and Logging:** KServe integrates with logging and monitoring systems to track model performance and detect issues.

![](assets/kserve_4.png)

---

## **How KServe Integrates with Kubernetes**
![](assets/kserve_3.png)

KServe is built on top of Kubernetes, leveraging its robust capabilities for container management. Here's how KServe integrates with Kubernetes:

- **InferenceServices:** KServe introduces a concept called **InferenceService**, a Kubernetes Custom Resource Definition (CRD). CRDs extend Kubernetes' default capabilities, allowing you to manage new types of resources. InferenceServices define how models are served in Kubernetes.
- **Autoscaling via Knative:** KServe integrates with **Knative**, an extension to Kubernetes that automatically scales your models based on demand.
- **Networking and Routing with Istio:** KServe uses **Istio**, a service mesh tool, to manage the traffic flow between model versions, ensuring that requests are routed correctly even as you roll out updates.

By leveraging these tools, KServe makes it easy to deploy, manage, and scale machine learning models, abstracting away much of the complexity of managing Kubernetes directly.

---

## **Setting Up a GCP Kubernetes Cluster**

Setting up a Kubernetes cluster on **Google Cloud Platform (GCP)** using **Google Kubernetes Engine (GKE)** is straightforward. GKE allows you to quickly create a managed Kubernetes cluster that you can use to deploy your applications (in this case, KServe).

### **Step 1: Google Cloud Console**
To create a Kubernetes cluster using the Google Cloud Console, follow these steps:
1. **Log into Google Cloud Console:** Visit [Google Cloud Console](https://console.cloud.google.com/) and log in with your Google account.
2. **Navigate to Kubernetes Engine:** From the sidebar, click on "Kubernetes Engine."
3. **Create a Cluster:**
   - Click on "Create Cluster."
   - Choose the type of cluster you want. A **Zonal** cluster is easier to set up and good for learning purposes. Choose your preferred zone (for example, `us-central1-a`).
   - Adjust settings like the number of Nodes in the cluster. A smaller cluster is fine for initial experiments (e.g., 3 Nodes).

### **Step 2: Using `gcloud` Command-Line Tool**
Alternatively, you can create the Kubernetes cluster via the `gcloud` command-line tool:

```bash
gcloud container clusters create [CLUSTER_NAME] --zone [ZONE]
```
Replace `[CLUSTER_NAME]` with the name of your cluster and `[ZONE]` with the desired zone (e.g., `us-central1-a`).

This command creates a GKE cluster with default settings. You can specify additional options such as machine type, number of nodes, and more.

### Explanation of the Command:

- `gcloud container clusters create` is the command to create a new GKE cluster.
- `[CLUSTER_NAME]` specifies the name of your cluster.
- `--zone [ZONE]` defines where your cluster will run. GCP is divided into geographic regions and zones (e.g., `us-central1-a`).

---

## **Installation Guide for gcloud CLI and kubectl**

To manage GCP resources and Kubernetes clusters, you'll need to install two essential command-line tools: **gcloud CLI** (for interacting with Google Cloud) and **kubectl** (for managing Kubernetes clusters).

---

### **Installing `gcloud CLI`**

The `gcloud` command-line interface (CLI) lets you manage resources on GCP, including Kubernetes clusters.

1. **Download and Install:**

   Follow the instructions on the [Google Cloud SDK installation page](https://cloud.google.com/sdk/docs/install).

   For **Linux**, you can use the following commands:

   ```bash
   curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-386.0.0-linux-x86_64.tar.gz
   tar -xf google-cloud-cli-386.0.0-linux-x86_64.tar.gz
   ./google-cloud-sdk/install.sh
   ```

    For **Windows**, download the installer from the SDK page and follow the installation instructions.

2. **Initialize `gcloud`**
    After installation, run the following command to set up the CLI and log in to your Google account:

    ```bash
    ./google-cloud-sdk/bin/gcloud init
    ```

    This will guide you through selecting a project, setting the default region, and logging in.

3. **Add `gcloud` to your PATH**
    Ensure you add `gcloud` to your system’s PATH variable so you can use the command without specifying its full path.

---

### **Installing `kubectl`**

    `kubectl` is the command-line tool used to interact with Kubernetes clusters. Once installed, you can use it to deploy, manage, and inspect your cluster.

    1. **Using `gcloud` CLI**
    Once the Google Cloud SDK is installed, you can install `kubectl` by running:

    ```bash
    gcloud components install kubectl
    ```
    2. **Verify the Installation:**
    After installation, run the following command to check if `kubectl` was installed successfully:

    ```bash
    kubectl version --client
    ```
    3. **Alternative Methods:**
        - You can also install kubectl using package managers like **`apt`**, **`yum`**, or **`brew`** for macOS

## **Conclusion**

In this guide, we introduced you to KServe and its integration with Kubernetes. We also demonstrated how to set up a GCP-based Kubernetes cluster using GKE. In our next guide, we'll dive deeper into installing KServe on this cluster.

## **References**

For more detailed information, please refer to the official documentation:

- [KServe Documentation](https://kserve.github.io/website/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)


