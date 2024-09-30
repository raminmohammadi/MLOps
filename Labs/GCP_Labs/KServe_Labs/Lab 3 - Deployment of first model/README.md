## Deploying Your First Model with KServe

Welcome to the ReadMe on deploying your first machine learning model using KServe. This tutorial will take you through creating an InferenceService with a pre-trained Scikit-learn Iris model, understanding the YAML configuration, and sending test inference requests.

### Understanding InferenceService YAML Configuration

The YAML configuration file is crucial as it defines how your model will be deployed and served. Below are the key components of the configuration:

- **apiVersion**: Specifies the KServe API version.
- **kind**: Set to `InferenceService`, indicating that we're deploying a model.
- **metadata**: Defines the name and namespace for the deployment.
- **spec**: Contains the `predictor` section where we specify the model type (Scikit-learn) and provide the `storageUri` for the model's location.

Here is a snippet of the YAML file:

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-iris
  namespace: kserve-test
spec:
  predictor:
    sklearn:
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1Gi"
```

For the complete InferenceService code, please refer to the YAML file provided in this repository.

### Deploying the Model

To deploy your model, apply the YAML configuration using the following command:

```bash
kubectl apply -f sklearn-iris.yaml
```
### Verifying Deployment

After deploying, verify that your service is running by checking its status with:

```bash
kubectl get inferenceservices sklearn-iris -n kserve-test
```

The output should indicate that your service is ready and provide a URL for accessing it.

**Determine External Load Balancer Support**

Execute the following command to determine if your Kubernetes cluster is running in an environment that supports external load balancers:

```bash
kubectl get svc istio-ingressgateway -n istio-system
```

If the `EXTERNAL-IP` value is set, your environment has an external load balancer that you can use for the ingress gateway. To set up environment variables for the ingress host and port, use the following commands:

```bash
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
```
### Sending Test Inference Requests

![img.png](assets/model_deployment.png)

To test your deployed model, send a test inference request using `curl`. Here's how you can do it:

```bash
SERVICE_HOSTNAME=$(kubectl get inferenceservice sklearn-iris -n kserve-test -o jsonpath='{.status.url}' | cut -d "/" -f 3)
 ```
```bash
curl -v -H "Host: ${SERVICE_HOSTNAME}" http://<INGRESS_HOST>:<INGRESS_PORT>/v1/models/sklearn-iris:predict -d @./iris-input.json
```

Ensure you have an input JSON file (`iris-input.json`) with sample data for prediction. The response will contain the predicted class for your input data.

### Conclusion

In this guide, we successfully deployed our first machine learning model using KServe and sent test inference requests.