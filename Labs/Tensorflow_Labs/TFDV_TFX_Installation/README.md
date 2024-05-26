# [Toturial Video](https://www.youtube.com/watch?v=xaSLeJzzJbI&list=PLcS4TrUUc53LeKBIyXAaERFKBJ3dvc9GZ&index=7)

# Approach 1


**TFXInstallation:**

- pip3 install --upgrade virtualenv
- python3 -m venv my_tfx
- source my_tfx/bin/activate
- pip install --upgrade pip setuptools wheel
- pip install ml-metadata==1.11.0
- pip install tfx==1.14.0 --no-dependencies
- python -c "import tfx;print(tfx.__version__)"

--------------------------------------------------------------

**TFDVInstallation:
Miniforge3File:** Link
- chmod +x ~/Downloads/Miniforge3-MacOSX-arm64.sh
- sh ~/Downloads/Miniforge3-MacOSX-arm64.sh
- source ~/miniforge3/bin/activate
- conda create -n tf python=3.9
- conda activate tf
- conda install -c apple tensorflow-deps
- python -m pip install tensorflow-macos==2.9
- python -m pip install tensorflow-metal
- pip install --upgrade tensorflow-macos tensorflow-metal
- import tensorflow as tf
- print(tf.config.list_physical_devices('GPU'))

--------------------------------------------------------------

# Approach 2
## TFDV Installation
To Install TFDV make sure you have activated a new virtual environment and ensure if the Python
version is Python 3.9. Once done, Install the python 3.9 dev version using the following command
First ensure that you are on the latest version of pip by running this command
Following that install the latest version of pyfarmhash using the following command
Post this you can install the TFDV library using pip without any errors

To visualize the components run
- pip install --upgrade pip
- sudo apt-get install python3.9-dev
- pip install pyfarmhash
- pip install tensorflow-data-validation
- pip install tensorflow-data-validation[visualization]
