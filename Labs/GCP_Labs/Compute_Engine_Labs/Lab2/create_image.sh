gcloud compute images create imdb-sentiment-analysis-image \
    --project=cloud-compute-labs \
    --source-disk=imdb-sentiment-analysis-vm-restored \
    --source-disk-zone=us-central1-a \
    --storage-location=us