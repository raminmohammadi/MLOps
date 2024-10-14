## Installing KServe on Google Cloud Platform (GCP)

This guide will walk you through installing **KServe** on a **Kubernetes** cluster hosted on **Google Cloud Platform (GCP)**. We will cover setting up **Istio**, **Cert Manager**, and deploying **KServe** in **RawDeployment** mode.

![](assets/kserver_main.png)

---

### Setting Up Your Environment

Before starting, ensure you have a **Kubernetes** cluster set up on **GCP** using **Google Kubernetes Engine (GKE)**. If you haven’t done this yet, refer to the previous documentation or videos for detailed instructions on setting up the cluster.

---

### Prerequisites

- **Google Cloud SDK**: Ensure you have the `gcloud` command-line tool installed and configured. You can refer to the [Google Cloud SDK installation guide](https://cloud.google.com/sdk/docs/install) for installation instructions.

- **Kubernetes Cluster**: Set up a Kubernetes cluster on **GCP** using **GKE**. This will serve as the environment where KServe will be deployed.

- **kubectl**: Ensure you have the `kubectl` CLI installed to interact with your Kubernetes cluster. It can be installed with the **Google Cloud SDK** or separately.

---

### Connect to Your Cluster

To connect to your Kubernetes cluster, use the following command:

```bash
gcloud container clusters get-credentials [CLUSTER_NAME] --zone [ZONE]
```

### Explanation:

This command retrieves the credentials and configuration information for your cluster, allowing `kubectl` to interact with it.  
Replace `[CLUSTER_NAME]` with the name of your Kubernetes cluster and `[ZONE]` with its zone (e.g., `us-central1-a`).

---

### Setting Up Istio

![img.png](assets/istio_cover.png)

Istio is a service mesh that provides traffic management, security, and observability. KServe relies on Istio for traffic routing and scaling. Make sure your Kubernetes version is compatible with the recommended Istio version (for example, for Kubernetes 1.27, use Istio 1.18 or 1.19).

---

### Download and Install Istio

1. **Download Istio**: Download the appropriate Istio package using this command.


   ```bash
   curl -L https://istio.io/downloadIstio | sh -
   ```

2. **Move to the Istio Package Directory**: Change your working directory to the newly downloaded Istio package.

   ```bash
   cd istio-1.23.2
   ```

**Explanation**: After extracting Istio, this command moves you into the directory where Istio’s binary and configuration files are located.

   ```bash
   export PATH=$PWD/bin:$PATH
   ```

3. **Add `istioctl` to Your Path**: Add the `istioctl` client to your system’s PATH to make the Istio command available.

   ```bash
   istioctl install
   ```

**Explanation**: This command temporarily adds the `istioctl` binary to your PATH, enabling you to use the Istio CLI commands directly.


   ```bash
   kubectl --namespace istio-system get service istio-ingressgateway
   ```

4. **Install Istio Using the Default Profile**: Run this command to install Istio with default configurations.

   ```bash
   istioctl install
   ```

**Explanation**: `istioctl install` installs Istio on your Kubernetes cluster using the default settings.

5. **Fetch External IP Address or CNAME**: After installation, fetch the external IP address or CNAME of the Istio Ingress Gateway.

   ```bash
   kubectl --namespace istio-system get service istio-ingressgateway
   ```

**Explanation**: This command retrieves information about the Istio ingress service, which is responsible for routing external traffic into your cluster.

---

### Create IngressClass Resource

Once Istio is installed, create an **IngressClass** resource to allow traffic routing with Istio. Use the following YAML configuration.

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: istio
spec:
  controller: istio.io/ingress-controller
```

**Explanation**: This configuration creates an `IngressClass` named `istio`, specifying that it should be managed by the Istio ingress controller. This allows Kubernetes to route traffic via Istio’s ingress.


### Installing Cert Manager
![img.png](assets/cert-manager.png)


**Cert Manager** is a powerful Kubernetes add-on that automates the management and issuance of **TLS certificates**. It is essential for provisioning and renewing certificates, particularly when using webhooks in production environments, like those required by KServe.

Cert Manager helps manage the lifecycle of certificates by working with various Certificate Authorities (CA) such as **Let’s Encrypt**. Certificates are necessary for securing network communication, ensuring that communication between your Kubernetes resources is encrypted and secure.

#### Install Cert Manager

To install Cert Manager, you can apply its preconfigured static configuration.

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.3/cert-manager.yaml
```

**Explanation**: This command pulls the YAML configuration file from the official Cert Manager GitHub repository and applies it to your cluster, creating the necessary resources (CustomResourceDefinitions, webhooks, etc.) for Cert Manager to operate.

Cert Manager is now ready to handle certificates for internal services and webhooks. For additional configuration options, refer to the [Cert Manager installation guide](https://cert-manager.io/docs/installation/).

---

### Installing KServe

With Istio and Cert Manager set up, it’s time to install **KServe**, which provides model serving capabilities in your Kubernetes cluster. KServe will manage machine learning models, handle requests, and serve responses, making it a critical component for ML-driven services.

#### Apply KServe YAML

To install KServe, you need to apply the official KServe YAML file.

```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml
```

**Explanation**: This command applies the official KServe configuration YAML file to your Kubernetes cluster. The configuration includes all the necessary resources and services required to get KServe up and running. These resources include:
- **InferenceServices** for serving models.
- **CustomResourceDefinitions (CRDs)** to manage the lifecycle of the machine learning models.

Once installed, KServe will be able to handle the deployment and scaling of ML models on your cluster.

---

#### Install Default Serving Runtimes

KServe supports a wide range of machine learning frameworks such as **TensorFlow**, **PyTorch**, and **Scikit-learn**. To make use of these frameworks, you need to install the default serving runtimes.

```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve-cluster-resources.yaml
```

**Explanation**: This command installs KServe's default model runtimes. These runtimes provide the environment for serving machine learning models. By applying the provided YAML, the runtime environments for these frameworks (e.g., TensorFlow Serving) are set up so that your models can be deployed and served efficiently.

---

### Configuring Deployment Mode and Ingress

By default, KServe uses **Knative** for deploying models. In this guide, we'll switch to **RawDeployment** mode, which bypasses Knative. RawDeployment mode directly manages Kubernetes resources for model deployment, which can offer more flexibility.

#### Set RawDeployment as Default Deployment Mode

To set RawDeployment mode as the default for KServe, you need to patch the KServe configuration.

```bash
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic -p '{"data": {"deploy": "{\"defaultDeploymentMode\": \"RawDeployment\"}"}}'
```

**Explanation**: This command modifies KServe's configuration by patching the **ConfigMap** named `inferenceservice-config`. It sets the `defaultDeploymentMode` to `RawDeployment`, ensuring that models are deployed without relying on Knative.

#### Update Ingress Configuration

To ensure that KServe uses **Istio** for ingress traffic management, you’ll need to update the ingress configuration. You can either update the ingress configuration directly with YAML or apply a patch.

```yaml
ingress: |-
  {
    "ingressClassName": "istio",
    "ingressGateway": "istio-system/istio-ingressgateway",
    "ingressService": "istio-ingressgateway.istio-system.svc.cluster.local"
  }
```

Alternatively, apply this patch:


```bash
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic -p '{"data": {"ingress": "{\"ingressClassName\": \"istio\", \"ingressGateway\": \"istio-system/istio-ingressgateway\", \"ingressService\": \"istio-ingressgateway.istio-system.svc.cluster.local\"}"}}'
```

**Explanation**: This command updates KServe’s **ConfigMap** to configure the Istio ingress gateway for managing inbound traffic to your ML models. It ensures that all model inference requests are routed through the Istio ingress controller.

---

### Verifying Installation

Once all components are installed, it’s essential to verify that everything is running as expected. You can check the status of the pods in the **Istio**, **Cert Manager**, and **KServe** namespaces by listing the running pods in each respective namespace.

```bash
kubectl get pods -n istio-system
kubectl get pods -n cert-manager
kubectl get pods -n kserve-system
```

**Explanation**: These commands list the running pods in the respective namespaces. You should see all pods in a `Running` or `Completed` state. If any pods are stuck in an `Error` or `CrashLoopBackOff` state, there may be an issue with the installation that needs to be addressed.

---

### Conclusion

In this guide, we walked through the installation of **KServe** on **Google Cloud Platform (GCP)** using **RawDeployment** mode, along with **Istio** and **Cert Manager**. With this setup, you are now ready to deploy and serve machine learning models using KServe.

---

### References:
- https://cloud.google.com/sdk/docs/install
- https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/
- https://kserve.github.io/website/latest/admin/kubernetes_deployment/
- https://cert-manager.io/docs/installation/kubectl/
- https://cert-manager.io/docs/installation/
