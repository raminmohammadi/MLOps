import json
import requests
import streamlit as st
from pathlib import Path
from streamlit.logger import get_logger

# If you start the fast api server on a different port
# make sure to change the port below
FASTAPI_BACKEND_ENDPOINT = "http://localhost:8000"
# Make sure you have iris_model.pkl file in FastAPI_Labs/src folder.
# If it's missing run train.py in FastAPI_Labs/src folder 
FASTAPI_IRIS_MODEL_LOCATION = Path(__file__).resolve().parents[2] / 'FastAPI_Labs' / 'src' / 'iris_model.pkl'

# streamlit logger
LOGGER = get_logger(__name__)

def run():
    # Set the main dashboard page browser tab title and icon
    st.set_page_config(
        page_title="Iris Flower Prediction Demo",
        page_icon="🪻",
    )

    # Build the sidebar first
    # This sidebar context gives access to work on elements in the side panel
    with st.sidebar:
        # Check the status of backend
        try:
            # Make sure fast api is running. Check the lab for guidance on getting
            # the server up and running
            backend_request = requests.get(FASTAPI_BACKEND_ENDPOINT)
            # If backend returns successful connection (status code: 200)
            if backend_request.status_code == 200:
                # This creates a green box with message
                st.success("Backend online ✅")
            else:
                # This creates a yellow bow with message
                st.warning("Problem connecting 😭")
        except requests.ConnectionError as ce:
            LOGGER.error(ce)
            LOGGER.error("Backend offline 😱")
            # Show backend offline message
            st.error("Backend offline 😱")

        st.info("Configure parameters")
        # Set the values
        # sepal_length = st.slider("Sepal Length",4.3, 7.9, 4.3, 0.1, help="Sepal length in centimeter (cm)", format="%f")
        # sepal_width = st.slider("Sepal Width",2.0, 4.4, 2.0, 0.1, help="Sepal width in centimeter (cm)", format="%f")
        # petal_length = st.slider("Petal Length",1.0, 6.9, 1.0, 0.1, help="Petal length in centimeter (cm)", format="%f")
        # petal_width = st.slider("Petal Width",0.1, 2.5, 0.1, 0.1, help="Petal width in centimeter (cm)", format="%f")
        
        # Take JSON file as input
        test_input_file = st.file_uploader('Upload test prediction file',type=['json'])

        # Check if client has provided input test file
        if test_input_file:
            # Quick preview functionality for JSON input file
            st.write('Preview file')
            test_input_data = json.load(test_input_file)
            st.json(test_input_data)
            # Session is necessary, because the sidebar context acts within a 
            # scope, so to access information outside the scope
            # we need to save the information into a session variable
            st.session_state["IS_JSON_FILE_AVAILABLE"] = True
        else:
            # If user adds file, then performs prediction and then removes
            # file, the session var should revert back since file 
            # is not available
            st.session_state["IS_JSON_FILE_AVAILABLE"] = False
            
        # Predict button
        predict_button = st.button('Predict')

    # Dashboard body
    # Heading for the dashboard
    st.write("# Iris Flower Prediction! 🪻")
    # If predict button is pressed
    if predict_button:
        # check if file is available
        if "IS_JSON_FILE_AVAILABLE" in st.session_state and st.session_state["IS_JSON_FILE_AVAILABLE"]:
            # Check if iris_model.pkl is in FastAPI folder
            if FASTAPI_IRIS_MODEL_LOCATION.is_file():
                # The input needs to be converted from dictionary
                # to JSON since content exchange format type is set
                # as JSON by default
                # client_input = json.dumps({
                #     "petal_length": petal_length,
                #     "sepal_length": sepal_length,
                #     "petal_width": petal_width,
                #     "sepal_width": sepal_width
                # })
                client_input = json.dumps(test_input_data['input_test'])
                try:
                    # This holds the result. Acts like a placeholder
                    # that we can fill and empty as required
                    result_container = st.empty()
                    # While the model predicts show a spinner indicating model is
                    # running the prediction
                    with st.spinner('Predicting...'):
                        # Send post request to backend predict endpoint
                        predict_iris_response = requests.post(f'{FASTAPI_BACKEND_ENDPOINT}/predict', client_input)
                    # If prediction status OK
                    if predict_iris_response.status_code == 200:
                        # Convert response from JSON to dictionary
                        iris_content = json.loads(predict_iris_response.content)
                        start_sentence = "The flower predicted is: "
                        if iris_content["response"] == 0:
                            result_container.success(f"{start_sentence} setosa")
                        elif iris_content["response"] == 1:
                            result_container.success(f"{start_sentence} versicolor")
                        elif iris_content["response"] == 2:
                            result_container.success(f"{start_sentence} virginica")
                        else:
                            result_container.error("Some problem occured while prediction")
                            LOGGER.error("Problem during prediction")
                    else:
                        # Pop up notification at bottom-left if backend is down
                        st.toast(f':red[Status from server: {predict_iris_response.status_code}. Refresh page and check backend status]', icon="🔴")
                except Exception as e:
                    # Pop up notification if backend is down
                    st.toast(':red[Problem with backend. Refresh page and check backend status]', icon="🔴")
                    LOGGER.error(e)
            else:
                # Message for iris_model.pkl not found
                LOGGER.warning('iris_model.pkl not found in FastAPI Lab. Make sure to run train.py to get the model.')
                st.toast(':red[Model iris_model.pkl not found. Please run the train.py file in FastAPI Lab]', icon="🔥")
        else:
            # Message for invalid JSON file
            LOGGER.error('Provide a valid JSON file with input_test field')
            st.toast(':red[Please upload a JSON test file. Check data folder for test file.]')

if __name__ == "__main__":
    run()