gcloud beta compute instance-groups managed create imdb-mig \
    --project=cloud-compute-labs \
    --base-instance-name=imdb-mig \
    --template=projects/cloud-compute-labs/regions/#regions/instanceTemplates/#name-of-template \
    --size=1 \
    --zone=#zone_name \
    --default-action-on-vm-failure=repair \
    --no-force-update-on-repair \
    --standby-policy-mode=manual \
    --list-managed-instances-results=pageless \
&& \
gcloud beta compute instance-groups managed set-autoscaling imdb-mig \
    --project=cloud-compute-labs \
    --zone=us-central1-c \
    --mode=on \
    --min-num-replicas=1 \
    --max-num-replicas=3 \
    --target-cpu-utilization=0.6 \
    --cpu-utilization-predictive-method=none \
    --cool-down-period=120