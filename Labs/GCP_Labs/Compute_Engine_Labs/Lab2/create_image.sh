gcloud compute images create #name-of-the-image \
    --project=#project_id \
    --source-disk=#name-of-vm \
    --source-disk-zone=#zone-name \
    --storage-location=us