# This script performs the following Kubernetes operations:
# 1. Checks the rollout status of the deployment named 'fastapi-app' to ensure it has been successfully deployed.
# 2. Lists all the pods in the current namespace to provide an overview of running pods.
# 3. Retrieves detailed information about all pods, including node assignments and IP addresses, using the wide output format.

kubectl rollout status deploy fastapi-app
kubectl get pods
kubectl get pod -o wide