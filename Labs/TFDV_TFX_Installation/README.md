# Toturial Video [linke](https://www.youtube.com/watch?v=xaSLeJzzJbI&list=PLcS4TrUUc53LeKBIyXAaERFKBJ3dvc9GZ&index=7)

# Approach 1


**TFXInstallation:**

- pip3install--upgradevirtualenv

- python3-mvenvmy_tfx
- sourcemy_tfx_env/bin/activate
- pipinstall--upgradepipsetuptoolswheel
- pipinstallml-metadata==1.11.
- pipinstalltfx==1.14.0--no-dependencies
- python-c"importtfx;print(tfx.__version__)"

--------------------------------------------------------------

**TFDVInstallation:
Miniforge3File:** Link
- chmod+x~/Downloads/Miniforge3-MacOSX-arm64.sh
- sh~/Downloads/Miniforge3-MacOSX-arm64.sh
- source~/miniforge3/bin/activate
- condacreate-ntfpython=3.
- condaactivatetf
- condainstall-cappletensorflow-deps
- python-mpipinstalltensorflow-macos==2.
- python-mpipinstalltensorflow-metal
- pipinstall--upgradetensorflow-macostensorflow-metal
- importtensorflowastf
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
