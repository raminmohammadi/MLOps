# Containerized Application Deployment on GKE

This guide explains how to deploy a simple FastAPI application to Google Kubernetes Engine (GKE) using Kubernetes manifests and `kubectl`. The deployment includes basic configurations like setting replicas, applying labels, and establishing services to expose the application.

You can watch the toturial video at [Kubernetes-lab2](https://www.youtube.com/watch?v=3NOCchsRlog)


## Prerequisites

- Google Cloud account
- GKE cluster set up and available
- `kubectl` configured to interact with your GKE cluster
- Docker image of the FastAPI application uploaded to a container registry (e.g., Google Container Registry) or you can use the already publically available docker image `heyitsrj/mlops-fastapi-app:v3`

## Deployment Steps

### 1. Create Kubernetes Manifests

You will need to create at least two manifests: one for the Deployment and another for the Service.

### 2. Deploying the Application

Run the following kubectl commands to apply the manifests, creating the Deployment and Service in your GKE cluster.

```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 3. Verify the deployment

Check the status of your deployment and ensure that your pods are running:

```bash
kubectl get deployments -n <namespace>
kubectl get pods -n <namespace>
```

### 4. Access the Application

Once the Service is up, get the external IP address to access your FastAPI application:

```bash
kubectl get service -n <namespace>
```

The external IP listed under **`EXTERNAL-IP`** is where your FastAPI application is accessible.

## Important Deployment Terms

Understanding key Kubernetes terms can help you better manage and troubleshoot your deployments. Here are some important terms related to deploying applications in Kubernetes:

### Deployment
A **Deployment** provides declarative updates for Pods and ReplicaSets. You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. This structure allows you to easily scale and update your application.

### ReplicaSet
A **ReplicaSet** ensures that a specified number of pod replicas are running at any given time. It's mostly used by Deployments to orchestrate pod creation, deletion, and updates.

### Service
A **Service** in Kubernetes is an abstraction which defines a logical set of Pods bound by a policy by which to access them - such as a load balancer. Services allow your applications to receive traffic.

### Namespace
A **Namespace** provides a mechanism for isolating groups of resources within a single cluster. Namespaces are how you divide cluster resources between multiple users and applications.

### Kubectl
**Kubectl** is a command line tool for Kubernetes. It allows you to run commands against Kubernetes clusters to deploy applications, inspect and manage cluster resources, and view logs.

### ConfigMap and Secrets
**ConfigMaps** and **Secrets** are Kubernetes objects used to store non-confidential and confidential data, respectively. This data can be used by Pods or other system components. ConfigMaps are ideal for storing configuration settings and parameters, while Secrets are used for sensitive information.

### LoadBalancer
A **LoadBalancer** Service is a type of Service that distributes network traffic to the pods from an external source. It is typically provisioned by an external cloud provider like Google Cloud, AWS, or Microsoft Azure.

### Label and Selector
**Labels** are key/value pairs attached to objects, such as pods. **Selectors** are how you specify which pods a service or deployment should target. Labels and selectors are integral for managing components across a Kubernetes environment.


## **Conclusion**

You have now deployed a basic FastAPI application on GKE using Kubernetes. This setup includes a scalable deployment managed by Kubernetes and a Service that exposes your app to the internet.
