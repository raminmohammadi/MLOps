sudo apt-get update
sudo apt-get install -y python3 python3-pip python3.11-venv git
sudo mkdir -p /home/imdb-sentiment-analysis
sudo chmod -R 777 /home/imdb-sentiment-analysis
cd /home/imdb-sentiment-analysis
git clone https://github.com/raminmohammadi/MLOps.git
cd /home/imdb-sentiment-analysis/MLOps/Labs/GCP_Labs/Compute_Engine_Labs/Lab2
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
