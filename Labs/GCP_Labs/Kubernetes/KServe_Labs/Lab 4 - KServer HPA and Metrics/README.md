# **Autoscaling with HPA and Debugging InferenceServices**
This lab wil will cover essential aspects of managing KServe deployments: configuring Horizontal Pod Autoscaling (HPA) for efficient resource utilization and ensuring service reliability through debugging and troubleshooting techniques. These labs will guide you through setting up autoscaling based on traffic and resource usage, as well as resolving common deployment issues to maintain high availability in production environments.

## **Prerequisites**

Before starting these labs, ensure that you have the following:

- A Google Cloud account and project.
- A Kubernetes cluster running on Google Kubernetes Engine (GKE).
- KServe installed on your GKE cluster.
- Basic knowledge of Kubernetes and KServe.

## **Tools Required:**

- **`gcloud`** CLI
- **`kubectl`** CLI
- Access to Google Cloud Storage (GCS) for storing model artifacts.

## **Autoscaling with Horizontal Pod Autoscaler (HPA)**

In this lab, you will learn how to configure autoscaling for KServe InferenceServices using Kubernetes' Horizontal Pod Autoscaler (HPA). You will also explore KServe’s scale-to-zero capability, which helps optimize resource usage when there is no traffic.

### **Key Concepts**

- **Horizontal Pod Autoscaler (HPA)**: Automatically scales the number of pods based on observed CPU utilization or other custom metrics.
- **Scale-to-zero**: A feature in KServe that scales down the number of replicas to zero when there is no traffic, saving resources.
- **Monitoring Tools**: Use tools like Prometheus/Grafana or Google Cloud Monitoring to observe key metrics such as CPU usage, memory utilization, and request latency.

### **Configuring Autoscaling with Horizontal Pod Autoscaler (HPA)**

KServe integrates with Kubernetes HPA to scale based on CPU utilization or request load.

1. Create an HPA YAML configuration for your InferenceService:

    ```yaml
    apiVersion: autoscaling/v1
    kind: HorizontalPodAutoscaler
    metadata:
      name: sklearn-iris-hpa
      namespace: kserve-test
    spec:
      scaleTargetRef:
        apiVersion: serving.kserve.io/v1beta1
        kind: InferenceService
        name: sklearn-iris
      minReplicas: 1
      maxReplicas: 5
      targetCPUUtilizationPercentage: 80  # Scale when CPU utilization exceeds 80%
    ```

2. Apply the HPA configuration:

   `kubectl apply -f sklearn-iris-hpa.yaml`

3. Verify that HPA is working by checking the status:

   `kubectl get hpa sklearn-iris-hpa -n kserve-test`


## **Common Issues Encountered During Deployment**

1. **Issue #1: InferenceService Not Ready**
    - Symptom: The service is stuck in a non-ready state.
    - Solution:
        - Check the status of the InferenceService:

          `kubectl get inferenceservices sklearn-iris -n kserve-test`

        - Investigate pod logs for errors:

          `kubectl logs <pod-name> -c &lt;container-name&gt; -n kserve-test`

2. **Issue #2: Model Download Failure**
    - Symptom: The model fails to download from cloud storage.
    - Solution:
        - Check the logs of the storage initializer container:

          `kubectl logs <pod-name> -c storage-initializer -n kserve-test`

3. **Issue #3: Out Of Memory (OOM) Errors**
    - Symptom: The pod crashes due to insufficient memory.
    - Solution:
        - Increase the memory limits in your InferenceService YAML file under **`resources.limits.memory`**.

## **References**

Here are some useful references that were used while preparing these labs:

- [KServe Documentation](https://kserve.github.io/website/)
- [Kubernetes Horizontal Pod Autoscaler (HPA)](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Google Cloud Monitoring](https://cloud.google.com/monitoring)
- [Prometheus Operator Documentation](https://prometheus.io/docs/prometheus/latest/getting_started/)
- [Grafana Documentation](https://grafana.com/docs/grafana/latest/getting-started/)