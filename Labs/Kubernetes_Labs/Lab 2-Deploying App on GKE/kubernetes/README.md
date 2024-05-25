## Kubernetes Manifest

Kubernetes manifests are essentially files in YAML or JSON format that describe the desired state of Kubernetes API objects within the cluster. The three most important components within the structure of a manifest file are **metadata**, **spec**, and **status**. 

- The metadata section includes essential information like the name and namespace of the object. 
- spec, or object specification, outlines the desired state for the object, specifying its properties and behavior.
- The status field is typically not included in the Kubernetes manifest files you create and apply, as it’s managed by the Kubernetes system itself to reflect the current state of the resources. However, once a resource is running, you can query its status using kubectl commands (more on this shortly).

All in all, **manifests** bring the power of declarative programming to infrastructure resource management. You tell Kubernetes what you want, and it handles the details of getting there, resulting in a more streamlined, efficient, and error-resilient infrastructure management process.

### Core Kubernetes Resource Kinds:

- Pod: Basic unit of deployment, representing a group of one or more containers.
- Service: Abstracts a set of pods and provides a stable endpoint for them.
- ReplicationController: Ensures a specified number of pod replicas are running at any one time.
- ReplicaSet: The next-generation ReplicationController, usually used by Deployments.
- Deployment: Manages a ReplicaSet and provides declarative updates to applications.
- StatefulSet: Manages stateful applications, providing guarantees about the ordering and uniqueness of pod replicas.
- DaemonSet: Ensures that all or some nodes run a copy of a pod.
- Job: Creates one or more pods and ensures they successfully terminate.
- CronJob: Manages time-based jobs, running them on a schedule.
- ConfigMap: Provides configuration data to pods.
- Secret: Stores sensitive data, such as passwords, OAuth tokens, and ssh keys.
- PersistentVolume: Represents a piece of storage in the cluster.
- PersistentVolumeClaim: Represents a request for storage by a user.
- Namespace: Provides a way to divide cluster resources between multiple users.
- Node: Represents a node in a Kubernetes cluster.
- ServiceAccount: Provides an identity for processes running in a pod.
- Role: Grants permissions within a namespace.
- ClusterRole: Grants permissions cluster-wide.
- RoleBinding: Grants permissions defined in a Role to a user or set of users within a namespace.
- ClusterRoleBinding: Grants permissions defined in a ClusterRole to a user or set of users cluster-wide.
- ResourceQuota: Defines resource usage limits for a namespace.
- LimitRange: Specifies constraints on resource requests and limits for a namespace.
- HorizontalPodAutoscaler: Automatically scales the number of pods in a deployment, replica set, or stateful set.
- PodDisruptionBudget: Defines policies to help administrators manage voluntary disruptions to pods.

### Namespace

Kubernetes namespaces help different projects, teams, or customers to share a Kubernetes cluster.

It does this by providing the following:

- A scope for Names.
- A mechanism to attach authorization and policy to a subsection of the cluster.

Use of multiple namespaces is optional, ex: one for production, one for deployment.

#### Understand the default namespace
By default, a Kubernetes cluster will instantiate a default namespace when provisioning the cluster to hold the default set of Pods, Services, and Deployments used by the cluster.

Assuming you have a fresh cluster, you can inspect the available namespaces by doing the following:

```bash
kubectl get namespaces
```

```bash
kubectl create -f https://k8s.io/examples/admin/namespace.yaml
```

Read more on Namespaces [namespaces-walkthrough](https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/)

## Deployment

A Deployment provides declarative updates for Pods and ReplicaSets.

You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.

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

### replicas

It specifies the desired number of pod instances (replicas) that should be running at any given time. By maintaining a specific number of replicas, Kubernetes ensures high availability and fault tolerance for your applications.

### Selector

the selector field is used to specify how to identify the pods that a particular controller (like a Deployment, ReplicaSet, or Service) should manage. It helps in grouping and selecting the set of pods that match certain criteria, typically based on labels.

### template

#### metadata.labels

 These labels are key-value pairs that help identify and organize pods. They are crucial for selectors, which use these labels to manage and match resources within the cluster.

#### spec.containers
 specifies information about container which we want to deploy. 


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