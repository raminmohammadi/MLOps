import streamlit as st
import requests
from PIL import Image

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS FOR STYLING
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF2E2E;
        border-color: #FF2E2E;
    }
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR CONFIGURATION
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg/1200px-Iris_versicolor_3.jpg", caption="Iris Versicolor")
    st.title("🌸 About the App")
    st.info(
        """
        This machine learning app predicts the **species** of an Iris flower based on its measurements.
        
        The model uses the classic Iris dataset to distinguish between:
        - **Setosa**
        - **Versicolor**
        - **Virginica**
        """
    )
    st.write("---")
    st.caption("Built with Streamlit & Cloud Run")

# 4. MAIN APP INTERFACE
st.title("🌿 Iris Species Predictor")
st.markdown("Adjust the sliders below to input the flower measurements.")

# Create a 2x2 grid for inputs using columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sepal Dimensions")
    sepal_length = st.slider('Sepal Length (cm)', 0.0, 10.0, 5.1)
    sepal_width = st.slider('Sepal Width (cm)', 0.0, 10.0, 3.5)

with col2:
    st.subheader("Petal Dimensions")
    petal_length = st.slider('Petal Length (cm)', 0.0, 10.0, 1.4)
    petal_width = st.slider('Petal Width (cm)', 0.0, 10.0, 0.2)

st.write("---")

# 5. PREDICTION LOGIC
if st.button('🔍 Predict Species'):
    
    # Visual loading spinner
    with st.spinner('Analyzing flower data...'):
        data = {
            'sepal_length': sepal_length,
            'sepal_width': sepal_width,
            'petal_length': petal_length,
            'petal_width': petal_width
        }
        
        try:
            # API Call
            response = requests.post('https://iris-app-1091239832875.us-east1.run.app/predict', json=data)
            
            if response.status_code == 200:
                prediction = response.json()['prediction']
                
                # Dynamic Result Display
                st.success("Prediction Complete!")
                
                # Layout for result
                res_col1, res_col2 = st.columns([1, 2])
                
                # Image mapping for results
                images = {
                    "Iris-setosa": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg/640px-Kosaciec_szczecinkowaty_Iris_setosa.jpg",
                    "Iris-versicolor": "https://upload.wikimedia.org/wikipedia/commons/2/27/Blue_Flag%2C_Ottawa.jpg",
                    "Iris-virginica": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Iris_virginica_2.jpg/1200px-Iris_virginica_2.jpg"
                }
                
                # Determine image to show (default to generic if name mismatch)
                img_url = images.get(prediction, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg/1200px-Iris_versicolor_3.jpg")

                with res_col1:
                    st.image(img_url, use_column_width=True)
                
                with res_col2:
                    st.header(f"It's an **{prediction}**!")
                    st.markdown(f"""
                    Based on the dimensions provided:
                    * **Sepal:** {sepal_length} x {sepal_width} cm
                    * **Petal:** {petal_length} x {petal_width} cm
                    """)
                    st.balloons()
            
            else:
                st.error(f'Server Error: {response.status_code}')
                
        except requests.exceptions.RequestException as e:
            st.error('Connection Error: Could not reach the prediction service.')