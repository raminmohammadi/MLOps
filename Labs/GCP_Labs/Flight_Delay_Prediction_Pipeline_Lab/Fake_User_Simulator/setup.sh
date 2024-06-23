sudo apt-get update
sudo apt-get install -y python3 python3-pip python3.11-venv git
sudo mkdir -p /home/user_simulator
sudo chmod 777 /home/user_simulator
cd /home/user_simulator
python3 -m venv venv
. venv/bin/activate
pip install pandas requests tqdm numpy