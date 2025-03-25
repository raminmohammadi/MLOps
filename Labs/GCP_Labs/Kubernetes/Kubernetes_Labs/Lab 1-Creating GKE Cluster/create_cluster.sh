gcloud beta container --project "kubernetes-labs-mlops" \
clusters create "mlops-lab-clusters" --region "us-central1" --tier "standard" \
--no-enable-basic-auth --cluster-version "1.31.6-gke.1020000" \
--release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" \
--disk-type "pd-balanced" --disk-size "100" --metadata disable-legacy-endpoints=true \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
--num-nodes "1" --logging=SYSTEM,WORKLOAD \
--monitoring=SYSTEM,STORAGE,POD,DEPLOYMENT,STATEFULSET,DAEMONSET,HPA,CADVISOR,KUBELET \
--enable-ip-alias --network "projects/kubernetes-labs-mlops/global/networks/default" \
--subnetwork "projects/kubernetes-labs-mlops/regions/us-central1/subnetworks/default" \
--no-enable-intra-node-visibility --default-max-pods-per-node "110" --enable-autoscaling \
--min-nodes "1" --max-nodes "2" --location-policy "BALANCED" --enable-ip-access \
--security-posture=standard --workload-vulnerability-scanning=disabled \
--no-enable-google-cloud-access --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
--enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 \
--binauthz-evaluation-mode=DISABLED --enable-managed-prometheus --enable-shielded-nodes \
--shielded-integrity-monitoring --no-shielded-secure-boot