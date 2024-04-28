import streamlit as st
import requests
import os

st.title('IRIS Prediction')

sepal_length = st.number_input('Sepal Length', min_value=0.0, max_value=10.0, step=0.1)
sepal_width = st.number_input('Sepal Width', min_value=0.0, max_value=10.0, step=0.1)
petal_length = st.number_input('Petal Length', min_value=0.0, max_value=10.0, step=0.1)
petal_width = st.number_input('Petal Width', min_value=0.0, max_value=10.0, step=0.1)

if st.button('Predict'):
    data = {
        'sepal_length': sepal_length,
        'sepal_width': sepal_width,
        'petal_length': petal_length,
        'petal_width': petal_width
    }
    try:
        response  = requests.post('https://iris-app-pbvf6ehg2a-ue.a.run.app/predict', json=data)
        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.success(f'Predicted species: {prediction}')
        else:
            st.error(f'Error occurred during prediction. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        st.error(f'Error occurred during prediction: {str(e)}')