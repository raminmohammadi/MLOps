# Flight Delay Prediction Pipeline

This FastAPI application predicts flight delays by utilizing a pre-trained machine learning model. The model, stored as a pickle file in Google Cloud Storage (GCS), is dynamically loaded into the application at runtime.

## Project Structure
```
Flight_Delay_Prediction_Pipeline_Lab/
├── backend/
│ ├── assets/ # Static files like images or JavaScript
│ ├── routers/ # Router files defining API endpoints
│ ├── schemas/ # Pydantic models for data validation
│ ├── utils/ # Utility modules
│ ├── .env # Environment variables
│ └── .env.example # Example environment configuration
├── kubernetes/
│ ├── configMap.yaml # Kubernetes ConfigMap
│ ├── deployment.yaml # Deployment configuration
│ ├── hpa.yaml # Horizontal Pod Autoscaler configuration
│ ├── kustomization.tmpl.yaml # Kustomization template for Kubernetes resources
│ ├── namespace.yaml # Namespace specification
│ └── service.yaml # Service definition
├── .dockerignore # Specifies patterns to ignore in Docker builds
├── Dockerfile # Defines the Docker container
├── main.py # Entry point for the FastAPI application
├── requirements.txt # Python dependencies
└── service_account.json # GCS service account credentials
```

## Setup

### Prerequisites

- Docker
- Kubernetes
- Google Cloud account with access to Google Cloud Storage

### Configuration

1. **Environment Variables:**
   Copy `.env.example` to `.env` and update the variables to match your environment, specifically your GCS bucket and credentials.

2. **GCS Credentials:**
   Ensure `service_account.json` contains the correct credentials to access the GCS bucket where the model pickle file is stored.

### Running the Application

```
uvicorn main:app --port 8080 --reload
```
## Deploying to Kubernetes
#### Apply Kubernetes Configurations:
Adjust the files in the kubernetes/ directory as needed, and then use kubectl to apply them:
```
kubectl apply -k kubernetes/deployment.yaml
```
#### Verify Deployment:
![GKE Deployment](./assets/deployment.png)
Check the deployment status with:
```
kubectl get all -n mlops
```

## Usage
Once deployed, the application exposes endpoints that allow users to predict flight delays based on the data provided in requests. For detailed API usage, refer to the Swagger UI at http://localhost:8000/docs.