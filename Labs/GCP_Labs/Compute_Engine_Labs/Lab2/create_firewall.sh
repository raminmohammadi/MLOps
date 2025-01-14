gcloud compute --project=#project_id firewall-rules create imdb-sentiment-analysis-vpc-allow-custom \\
--direction=INGRESS --priority=1000 --network=#vpc_network_name --action=ALLOW \\
--rules=tcp:22,tcp:80,tcp:8000 --source-ranges=0.0.0.0/0