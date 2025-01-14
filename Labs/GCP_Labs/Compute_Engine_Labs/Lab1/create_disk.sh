gcloud compute disks create mlops-disk \
    --project=cloud-compute-441619 \
    --type=pd-balanced \
    --size=10GB \
    --resource-policies=projects/cloud-compute-441619/regions/us-central1/resourcePolicies/default-schedule-1 \
    --zone=us-central1-a