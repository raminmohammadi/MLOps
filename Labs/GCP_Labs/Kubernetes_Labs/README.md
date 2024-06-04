## Important Deployment Terms

Understanding key Kubernetes terms can help you better manage and troubleshoot your deployments. Here are some important terms related to deploying applications in Kubernetes:

### Containers

In software engineering, a container is an executable unit of software that packages and runs an entire application, or portions of it, within itself.

Containers comprise not only the application’s binary files, but also libraries, runtimes, configuration files, and any other dependencies that the application requires to run optimally. Talk about self-sufficiency.

![Containers](assets/containers-vs-virtual-machine-architectures.png)

This design enables a container to be an entire application runtime environment unto itself.

As a result, a container isolates the application it hosts from the external environment it runs on. This enables applications running in containers to be built in one environment and deployed in different environments without compatibility problems.

Also, because containers share resources and do not host their own operating system, they are leaner than virtual machines (VMs). This makes deploying containerized applications much quicker and more efficient than on contemporary virtual machines.

### What Is A Containerized Application?
In cloud computing, a containerized application refers to an app that has been specially built using cloud-native architecture for running within containers. A container can either host an entire application or small, distributed portions of it (which are known as microservices).

Developing, packaging, and deploying applications in containers is referred to as containerization. Apps that are containerized can run in a variety of environments and devices without causing compatibility problems.

One more thing. Developers can isolate faulty containers and fix them independently before they affect the rest of the application or cause downtime. This is something that is extremely tricky to do with traditional monolithic applications.

### Pod
A **Pod** is the smallest deployable unit created and managed by Kubernetes. A pod is a group of one or more containers, with shared storage/network, and a specification for how to run the containers. Pods are ephemeral by nature.

- The pod is an additional level of abstraction that provides shared storage (volumes), IP address, communication between containers, and hosts other information about how to run application containers. 
![Pods](assets/pods.png)
- Containers that must communicate directly to function are housed in the same pod. These containers are also co-scheduled because they work within a similar context. Also, the shared storage volumes enable pods to last through container restarts because they provide persistent data.
- Kubernetes also scales or replicates the number of pods up and down to meet changing load/traffic/demand/performance requirements. Similar pods scale together.
- Another unique feature of Kubernetes is that rather than creating containers directly, it generates pods that already have containers.
- Also, whenever you create a K8s pod, the platform automatically schedules it to run on a Node. This pod will remain active until the specific process completes, resources to support the pod run out, the pod object is removed, or the host node terminates or fails.
- Each pod runs inside a Kubernetes node, and each pod can fail over to another, logically similar pod running on a different node in case of failure. And speaking of Kubernetes nodes.

### Node
A **Node** is a worker machine in Kubernetes, which may be a VM or a physical machine, depending on the cluster. Each node has the services necessary to run Pods and is managed by the master components.
![Nods](assets/node.png)

Each node also comprises three crucial components:

**Kubelet** – This is an agent that runs inside each node to ensure pods are running properly, including communications between the Master and nodes.

**Container runtime** – This is the software that runs containers. It manages individual containers, including retrieving container images from repositories or registries, unpacking them, and running the application.

**Kube-proxy** – This is a network proxy that runs inside each node, managing the networking rules within the node (between its pods) and across the entire Kubernetes cluster.

### Kubernetes Cluster
Nodes usually work together in groups. A **Kubernetes cluster** contains a set of work machines (nodes). The cluster automatically distributes workload among its nodes, enabling seamless scaling.

**Here’s that symbiotic relationship:**

- A cluster consists of several nodes. The node provides the compute power to run the setup. It can be a virtual machine or a physical machine. A single node can run one or more pods.
- Each pod contains one or more containers. A container hosts the application code and all the dependencies the app requires to run properly.


### Kubectl
**Kubectl** is a command line tool for Kubernetes. It allows you to run commands against Kubernetes clusters to deploy applications, inspect and manage cluster resources, and view logs.

To read more on how to install kubectl, please refer to [kubectl installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)


### Deployment
A **Deployment** provides declarative updates for Pods and ReplicaSets. You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. This structure allows you to easily scale and update your application.

### ReplicaSet
A **ReplicaSet** ensures that a specified number of pod replicas are running at any given time. It's mostly used by Deployments to orchestrate pod creation, deletion, and updates.

### Service
A **Service** in Kubernetes is an abstraction which defines a logical set of Pods bound by a policy by which to access them - such as a load balancer. Services allow your applications to receive traffic.

### Namespace
A **Namespace** provides a mechanism for isolating groups of resources within a single cluster. Namespaces are how you divide cluster resources between multiple users and applications.


### ConfigMap and Secrets
**ConfigMaps** and **Secrets** are Kubernetes objects used to store non-confidential and confidential data, respectively. This data can be used by Pods or other system components. ConfigMaps are ideal for storing configuration settings and parameters, while Secrets are used for sensitive information.

### LoadBalancer
A **LoadBalancer** Service is a type of Service that distributes network traffic to the pods from an external source. It is typically provisioned by an external cloud provider like Google Cloud, AWS, or Microsoft Azure.

### Label and Selector
**Labels** are key/value pairs attached to objects, such as pods. **Selectors** are how you specify which pods a service or deployment should target. Labels and selectors are integral for managing components across a Kubernetes environment.

