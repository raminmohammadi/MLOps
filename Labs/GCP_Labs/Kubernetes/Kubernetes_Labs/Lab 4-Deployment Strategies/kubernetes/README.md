Instead of using two separate Services (blue-service and green-service), use a single Service and switch the selector when you want to switch traffic.

```yaml
apiVersion: v1
kind: Service
metadata:
  namespace: mlops
  name: mlops-service  # Single service for traffic switching
spec:
  selector:
    app: blue-deploy  # Initially points to the blue deployment
  ports:
    - name: http
      port: 80
      targetPort: 8080
  type: LoadBalancer

```

```sh
kubectl patch service blue-service -n mlops -p '{"spec": {"selector": {"app": "green-deploy"}}}'

```