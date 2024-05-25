### Kubernetes Manifest

Kubernetes manifests are essentially files in YAML or JSON format that describe the desired state of Kubernetes API objects within the cluster. The three most important components within the structure of a manifest file are **metadata**, **spec**, and **status**. 

- The metadata section includes essential information like the name and namespace of the object. 
- spec, or object specification, outlines the desired state for the object, specifying its properties and behavior.
- The status field is typically not included in the Kubernetes manifest files you create and apply, as it’s managed by the Kubernetes system itself to reflect the current state of the resources. However, once a resource is running, you can query its status using kubectl commands (more on this shortly).

All in all, **manifests** bring the power of declarative programming to infrastructure resource management. You tell Kubernetes what you want, and it handles the details of getting there, resulting in a more streamlined, efficient, and error-resilient infrastructure management process.

You’ll use a kind (ex: deployment) for the following example because it’s the smallest compute unit you can deploy in a Kubernetes cluster.

Writing a manifest for a deployment is a straightforward process. First, you need to define the apiVersion, which indicates the Kubernetes API version that you’re using. Second, you need to specify the kind field to denote the type of object you want to create—in this case, a deployment. Next, you need to write the metadata section, which contains information about the deployment, such as its name and labels.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: mlops
  name: fastapi-app

```

The second portion corresponds to the object specification. The spec section outlines the behavior of the deployment. It’s here that you define the container(s) that the deployment will run. Each container needs an image and a name, like so:

```
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
          - name: fastapi-app-container
            image: heyitsrj/mlops-fastapi-app:v3
            imagePullPolicy: Always
            ports:
              - containerPort: 8080
```