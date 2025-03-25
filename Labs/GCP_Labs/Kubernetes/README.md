# 1. Create the Namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy the Backend
kubectl apply -f k8s/backend/backend-deployment.yaml
kubectl apply -f k8s/backend/backend-service.yaml

# 3. Deploy the Frontend
kubectl apply -f k8s/frontend/frontend-deployment.yaml
kubectl apply -f k8s/frontend/frontend-service.yaml

# 4. Apply Horizontal Pod Autoscalers
kubectl apply -f k8s/hpa/backend-hpa.yaml
kubectl apply -f k8s/hpa/frontend-hpa.yaml

# 5. Apply Network Policy (Ensure restricted communication)
kubectl apply -f k8s/network-policy/backend-access-policy.yaml
