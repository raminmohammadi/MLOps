gcloud compute disks create mlops-disk \
    --project=cloud-compute-labs \
    --type=pd-ssd \
    --size=10GB \
    --resource-policies=projects/cloud-compute-labs/regions/us-east1/resourcePolicies/default-schedule-1 \
    --region=us-east1 \
    --replica-zones=projects/cloud-compute-labs/zones/us-east1-d,projects/cloud-compute-labs/zones/us-east1-b