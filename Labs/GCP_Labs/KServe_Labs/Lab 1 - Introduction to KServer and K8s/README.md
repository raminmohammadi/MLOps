# **Introduction to KServe and Kubernetes**

## **By the end of this guide, you will have:**
A fully functional Kubernetes cluster running on GCP.
Installed and configured gcloud CLI and kubectl to interact with your cluster.
The foundational knowledge needed to deploy machine learning models using KServe in future labs.

## **What You Will Learn**

1. **Setting Up a GCP Kubernetes Cluster**:
    - You will learn how to create a managed Kubernetes cluster using Google Kubernetes Engine (GKE) via both the Google Cloud Console and the **`gcloud`** command-line tool.
2. **Installing gcloud CLI and kubectl**:
    - You will install the **`gcloud`** CLI for managing GCP resources and **`kubectl`** for interacting with your Kubernetes cluster.
3. **Preparing for KServe Deployment**:
    - This guide lays the groundwork for deploying KServe on your Kubernetes cluster in future steps.

## **Setting Up a GCP Kubernetes Cluster**

Setting up a Kubernetes cluster on **Google Cloud Platform (GCP)** using **Google Kubernetes Engine (GKE)** is straightforward. GKE allows you to quickly create a managed Kubernetes cluster that you can use to deploy your applications (in this case, KServe).

[Video](https://youtu.be/PpODtZbq3pc)


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


