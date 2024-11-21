# Creating a GKE Cluster

This guide provides instructions on how to create a Google Kubernetes Engine (GKE) cluster using both the Google Cloud Console and the command-line interface (CLI). Learn to set up a basic cluster with configurations such as cluster name, zone/region, and node pool settings.

You can watch the toturial video at [Kubernetes-lab1](https://www.youtube.com/watch?v=_z9ZdGnIVSE)

## Prerequisites

Before you begin, ensure you have the following:
- A Google Cloud Platform (GCP) account.
- `gcloud` CLI installed and configured. [Installation guide](https://cloud.google.com/sdk/docs/install-sdk). If you are using mac OS then you can simply use homebrew to install Google cloud CLI easily.
  `brew install --cask google-cloud-sdk`
- **Kubectl** installed on your local machine. [Installation guide](https://kubernetes.io/docs/tasks/tools/).

## Initializing gcloud CLI

Before using the `gcloud` CLI to create a GKE cluster, you must initialize it. This setup involves authenticating your account and setting the default project: `gcloud init`

In your browser, log in to your Google user account when prompted and click Allow to grant permission to access Google Cloud resources.

**Once this is done, out Google Cloud CLI client is initialized and ready for further use.
**
## Creating a GKE Cluster Using Google Cloud Console
### Step 1: Access the Google Cloud Console
Go to the [Google Cloud Console](https://console.cloud.google.com/).

### Step 2: Create a Cluster
1. Navigate to the Kubernetes Engine section, enable the **Kubernetes Engine API**.
2. Click on **Clusters**, then click **Create Cluster**.
3. Enter the **Cluster name**.
4. Choose the **Zone or Region** where you want your cluster to be deployed.
5. Configure the **Node Pools** settings including the number of nodes, machine type, and disk type.
6. Click **Create** to deploy your cluster.

## Managing Your Cluster

Once your cluster is up and running, you can manage it using either the Google Cloud Console or the `gcloud` CLI. Here are some common management tasks:

### Accessing the Cluster
1. To get credentials for your cluster and interact with it using `kubectl`,
   run:
   `gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE]`

2. Check the configuration of kubectl to ensure it is set to your new cluster:
   `kubectl config current-context`
3. You can now interact with your cluster using kubectl commands. For example, to view all nodes in the cluster, run:
   `kubectl get nodes` or `kubectl get ns`

## Kubectl Commands Cheatsheet
### Cluster Management
- `kubectl cluster-info`: Display master and service endpoints.
- `kubectl version`: Show client and server versions.
- `kubectl config view`: Get cluster configuration.
- `kubectl api-resources`: List available API resources.
- `kubectl api-versions`: List API versions.
- `kubectl get all --all-namespaces`: List everything in all namespaces.

### Daemonsets (ds)
- `kubectl get daemonset`: List daemonsets.
- `kubectl edit daemonset <name>`: Edit a daemonset.
- `kubectl delete daemonset <name>`: Delete a daemonset.
- `kubectl create daemonset <name>`: Create a daemonset.
- `kubectl describe ds <name> -n <namespace>`: Detailed state of a daemonset.

### Deployments (deploy)
- `kubectl get deployment`: List deployments.
- `kubectl describe deployment <name>`: Detailed state of a deployment.
- `kubectl edit deployment <name>`: Edit a deployment.
- `kubectl create deployment <name>`: Create a deployment.
- `kubectl delete deployment <name>`: Delete a deployment.
- `kubectl rollout status deployment <name>`: Rollout status of a deployment.

### Pods (po)
- `kubectl get pod`: List pods.
- `kubectl delete pod <name>`: Delete a pod.
- `kubectl describe pod <name>`: Detailed pod state.
- `kubectl exec <pod> -c <container> <command>`: Execute command in a pod's container.
- `kubectl logs <pod>`: Print pod logs.

### Namespaces (ns)
- `kubectl create namespace <name>`: Create a namespace.
- `kubectl get namespace <name>`: List namespaces.
- `kubectl describe namespace <name>`: Detailed namespace state.
- `kubectl delete namespace <name>`: Delete a namespace.

### Nodes (no)
- **List Nodes**: `kubectl get node`
- **Delete Node**: `kubectl delete node <node_name>`
- **Taint Node**: `kubectl taint node <node_name>`
- **Show Node Resource Usage**: `kubectl top node`
- **Cordon Node**: `kubectl cordon <node_name>`
- **Uncordon Node**: `kubectl uncordon <node_name>`
- **Drain Node**: `kubectl drain <node_name>`

### Secrets
- **Create Secret**: `kubectl create secret`
- **List Secrets**: `kubectl get secrets`
- **Describe Secrets**: `kubectl describe secrets`
- **Delete Secret**: `kubectl delete secret <secret_name>`

### Services (svc)
- **List Services**: `kubectl get services`
- **Describe Service**: `kubectl describe services`
- **Edit Service**: `kubectl edit services`
- **Expose Deployment as Service**: `kubectl expose deployment [deployment_name]`

### StatefulSets (sts)
- **List StatefulSets**: `kubectl get statefulset`
- **Delete StatefulSet**: `kubectl delete statefulset/[stateful_set_name] --cascade=false`

### Common Options
- **Output Format**: `kubectl get pods -o wide`
- **Specify Namespace**: `kubectl get pods -n=[namespace_name]`
- **Use Manifest File**: `kubectl create -f ./newpod.json`
- **Selector Filter**: `kubectl get nodes -l env=production`
