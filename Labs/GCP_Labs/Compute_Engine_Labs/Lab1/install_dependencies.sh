sudo apt install python3.11-venv
sudo chown -R $USER:$USER env/
source /env/bin/activate
python3 -m pip install -r requirements.txt
python3 airbnb_random_forest_regressor.py
