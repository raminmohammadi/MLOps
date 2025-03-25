# 1. Create the Namespace
kubectl apply -f kubernetes/namespace.yaml

# 2. Deploy the Backend
kubectl apply -f backend/kubernetes/backend-deployment.yaml
kubectl apply -f backend/kubernetes/backend-service.yaml

# 3. Deploy the Frontend
kubectl apply -f frontend/kubernetes/frontend-deployment.yaml
kubectl apply -f frontend/kubernetes/frontend-service.yaml

# 4. Apply Horizontal Pod Autoscalers
kubectl apply -f hpa/backend-hpa.yaml
kubectl apply -f hpa/frontend-hpa.yaml

# 5. Apply Network Policy (Ensure restricted communication)
kubectl apply -f network-policy/backend-access-policy.yaml
