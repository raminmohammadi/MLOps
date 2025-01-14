# gcloud compute instances create lab2 \
#     --project=cloud-compute-441619 \
#     --zone=us-central1-a \
#     --machine-type=e2-medium \
#     --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
#     --metadata=ssh-keys=r.mohammadi:ssh-rsa\ \
# AAAAB3NzaC1yc2EAAAADAQABAAABAQC2ybAxDch6IU\+jhZwzwubPnCs92SGOuiCehZ1EfK5yrTikd8ZgLUNq9SmKyNNFQk7dH/QLUKbdA/qjUJyQvqtBo2H15ktUKA2weWv89sMJpSD66\+pEob5k\+ZzGcPxUwqzdIsirLGPEJJ1TGwO2/gEflI1pBacel7e7R\+XQtqzOktxx7HG5gZQTPVXV4kcR2kr5vEnm7ol64a1NYCoXIAO1Nzra7WFs2Pz5cN2jvroEC6rct99SaggR2veSDRz0amlrjfjOmXj8pt8keCdCMWQ4j4mILYqZRJRwhp9VzXHenDe1ieP\+mea/SfSf1DP2Lmxgw28VYhVbHYQh4ig2GGmt\ r.mohammadi@northeastern.edu \
#     --maintenance-policy=MIGRATE \
#     --provisioning-model=STANDARD \
#     --service-account=928526277109-compute@developer.gserviceaccount.com \
#     --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
#     --create-disk=auto-delete=yes,boot=yes,device-name=lab1-part-1,disk-resource-policy=projects/cloud-compute-441619/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/debian-cloud/global/images/debian-12-bookworm-v20241112,mode=rw,size=10,type=pd-balanced \
#     --no-shielded-secure-boot \
#     --shielded-vtpm \
#     --shielded-integrity-monitoring \
#     --labels=goog-ec-src=vm_add-gcloud \
#     --reservation-affinity=any

gcloud compute instances create lab1-2 \
    --project=cloud-compute-441619 \
    --zone=us-central1-a \
    --machine-type=c2-standard-4 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --metadata=ssh-keys=r.mohammadi:ssh-rsa\ AAAAB3NzaC1yc2EAAAADAQABAAABAQC2ybAxDch6IU\+jhZwzwubPnCs92SGOuiCehZ1EfK5yrTikd8ZgLUNq9SmKyNNFQk7dH/QLUKbdA/qjUJyQvqtBo2H15ktUKA2weWv89sMJpSD66\+pEob5k\+ZzGcPxUwqzdIsirLGPEJJ1TGwO2/gEflI1pBacel7e7R\+XQtqzOktxx7HG5gZQTPVXV4kcR2kr5vEnm7ol64a1NYCoXIAO1Nzra7WFs2Pz5cN2jvroEC6rct99SaggR2veSDRz0amlrjfjOmXj8pt8keCdCMWQ4j4mILYqZRJRwhp9VzXHenDe1ieP\+mea/SfSf1DP2Lmxgw28VYhVbHYQh4ig2GGmt\ r.mohammadi@northeastern.edu \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=928526277109-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
    --create-disk=auto-delete=yes,boot=yes,device-name=lab1-2,disk-resource-policy=projects/cloud-compute-441619/regions/us-central1/resourcePolicies/default-schedule-1,image=projects/debian-cloud/global/images/debian-12-bookworm-v20241112,mode=rw,size=10,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any