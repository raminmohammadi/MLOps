gcloud compute snapshots create imdb-sentiment-analysis-vm-snapshot \
    --project=cloud-compute-labs \
    --source-disk=imdb-sentiment-analysis-vm \
    --source-disk-zone=us-central1-a \
    --storage-location=us