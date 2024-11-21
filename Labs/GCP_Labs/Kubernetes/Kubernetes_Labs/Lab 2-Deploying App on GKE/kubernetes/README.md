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

### Deployment

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

#### replicas

It specifies the desired number of pod instances (replicas) that should be running at any given time. By maintaining a specific number of replicas, Kubernetes ensures high availability and fault tolerance for your applications.

#### Selector

the selector field is used to specify how to identify the pods that a particular controller (like a Deployment, ReplicaSet, or Service) should manage. It helps in grouping and selecting the set of pods that match certain criteria, typically based on labels.

#### template

##### metadata.labels

 These labels are key-value pairs that help identify and organize pods. They are crucial for selectors, which use these labels to manage and match resources within the cluster.

##### spec.containers
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
            imagePullPolicy: Always # to use latest version of the image always
            ports:
              - containerPort: 8080
```


### Service

In Kubernetes, a Service is a method for exposing a network application that is running as one or more Pods in your cluster.

A key aim of Services in Kubernetes is that you don't need to modify your existing application to use an unfamiliar service discovery mechanism. You can run code in Pods, whether this is a code designed for a cloud-native world, or an older app you've containerized. You use a Service to make that set of Pods available on the network so that clients can interact with it.

If you use a Deployment to run your app, that Deployment can create and destroy Pods dynamically. From one moment to the next, you don't know how many of those Pods are working and healthy; you might not even know what those healthy Pods are named. Kubernetes Pods are created and destroyed to match the desired state of your cluster. Pods are ephemeral resources (you should not expect that an individual Pod is reliable and durable).

Each Pod gets its own IP address (Kubernetes expects network plugins to ensure this). For a given Deployment in your cluster, the set of Pods running in one moment in time could be different from the set of Pods running that application a moment later.

This leads to a problem: if some set of Pods (call them "backends") provides functionality to other Pods (call them "frontends") inside your cluster, how do the frontends find out and keep track of which IP address to connect to, so that the frontend can use the backend part of the workload?

The Service API, part of Kubernetes, is an abstraction to help you expose groups of Pods over a network. Each Service object defines a logical set of endpoints (usually these endpoints are Pods) along with a policy about how to make those pods accessible.

For example, consider a stateless image-processing backend which is running with 3 replicas. Those replicas are fungible—frontends do not care which backend they use. While the actual Pods that compose the backend set may change, the frontend clients should not need to be aware of that, nor should they need to keep track of the set of backends themselves.

The Service abstraction enables this decoupling.

Read more on service at [service](https://kubernetes.io/docs/concepts/services-networking/service/)

#### LoadBalancer

a LoadBalancer service type is used to expose a service externally using a cloud provider's load balancer. This service type is commonly used to distribute incoming traffic across multiple pods, ensuring high availability and scalability of applications.

```
apiVersion: v1
kind: Service
metadata:
  namespace: mlops
  name: fast-api-service
spec:
  selector:
    app: fastapi-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: LoadBalancer #

```