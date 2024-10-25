## Watch the tutorial video at [Toturial Video](https://www.youtube.com/watch?v=O0X6NoQyEf0)

Install the [google cloud CLI](https://cloud.google.com/sdk/docs/install) based on your operating system and make sure the gcloud command works 



```
gcloud init
```
Make sure you have authenticated with the correct email Id and selected the correct project id and region
```
gcloud auth login
```

Also make sure you have enabled the folllowing API's
1. Artifact Registry
2. Cloud build

In your GCP command line run:
```
gcloud services enable cloudbuild.googleapis.com

```

To dockerize the application run
Cloud Build takes the directory you are currently in (or the path you specify) and looks for a Dockerfile or other build instructions to create a Docker container.

```
gcloud builds submit --tag gcr.io/[YOUR_PROJ_ID]/iris-app
```  

Deploying container to Cloud Run service

```
gcloud run deploy iris-app --image gcr.io/[YOUR_PROJ_ID]/iris-app --platform managed --port 8501 --allow-unauthenticated   
```

Once the application is deployed you can update the deployed URL in your frontend source code (streamlit_app.py). then run 

```
streamlit run streamlit_app.py
```

