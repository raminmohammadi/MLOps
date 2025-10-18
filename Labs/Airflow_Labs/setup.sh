docker compose down -v   # removes containers and volumes
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose run airflow-cli airflow config list