gcloud compute instances create imdb-sentiment-analysis-vm-restored \
    --project=cloud-compute-labs \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=ssh-keys=r.mohammadi:ssh-rsa\ \
AAAAB3NzaC1yc2EAAAADAQABAAABAQDd7v6GH3/k1jRuIksihVyQyK\+S6tt8UaVb/yUAj4MJ2cjJUAQOufSTuepdNnIAJoJIEwbVOW0LcW\+HrIZFanXMnM\+c9eno24VJunY69Y3XaKAILRr/r2tc1vxIZrnGDcubQrsCfehaTV5bAN4bTuayW2p0zBpA4O2OMCDt3kHwznaJzqOrf\+qgc8IkiLK7/OVHWTGc/ri/CA5MVoRZP5z15OKSVKK8Y5vo/ZvB8n5m1d\+hEq8rGcipKnpzSD/JPZFonJMj/U1Jw2VkPgQ4fkkRzy4pnS31JVrfoJ\+QE\+GE8MtV56tOYCBrUGRfRl31Xldpzmd5XnEyHOtnuejR6jLv\ r.mohammadi@northeastern.edu \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=108010409596-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=imdb-sentiment-analysis-vm-restored,mode=rw,size=10,source-snapshot=https://www.googleapis.com/compute/v1/projects/cloud-compute-labs/global/snapshots/imdb-sentiment-analysis-vm-snapshot,type=pd-balanced \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any