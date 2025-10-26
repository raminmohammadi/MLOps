import streamlit as st
import pandas as pd
import requests
import json
from io import BytesIO

st.set_page_config(page_title="Iris Species Predictor", page_icon="🌸", layout="centered")
st.title("🌸 Iris Flower Species Prediction App")

PREDICT_URL = "http://127.0.0.1:8080/predict"      # your local Flask API
headers = {"Content-Type": "application/json"}

st.markdown(
    """
    This app connects to a Flask API that predicts the **Iris flower species**
    based on sepal and petal dimensions.  
    You can try single predictions or upload a CSV for batch results.
    """
)

option = st.sidebar.radio("Select Mode:", ["Single Prediction", "Batch Prediction (CSV)"])

if option == "Single Prediction":
    st.subheader("🔹 Enter Flower Measurements")

    sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, max_value=10.0, step=0.1)
    sepal_width  = st.number_input("Sepal Width (cm)",  min_value=0.0, max_value=10.0, step=0.1)
    petal_length = st.number_input("Petal Length (cm)", min_value=0.0, max_value=10.0, step=0.1)
    petal_width  = st.number_input("Petal Width (cm)",  min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Predict"):
        payload = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
        }

        try:
            response = requests.post(PREDICT_URL, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"🌼 Predicted species: **{prediction}**")
            else:
                st.error(f"❌ API Error: Status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Connection error: {str(e)}")

else:
    st.subheader("📂 Upload CSV for Batch Prediction")

    st.markdown(
        """
        **Required columns:**  
        `sepal_length`, `sepal_width`, `petal_length`, `petal_width`  
        """
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("✅ Uploaded data preview:")
        st.dataframe(df.head())

        if st.button("Run Batch Predictions"):
            predictions = []
            for _, row in df.iterrows():
                payload = {
                    "sepal_length": row["sepal_length"],
                    "sepal_width": row["sepal_width"],
                    "petal_length": row["petal_length"],
                    "petal_width": row["petal_width"],
                }

                try:
                    resp = requests.post(PREDICT_URL, data=json.dumps(payload), headers=headers)
                    if resp.status_code == 200:
                        pred = resp.json().get("prediction", "Error")
                    else:
                        pred = f"Error {resp.status_code}"
                except Exception as e:
                    pred = f"Error: {str(e)}"

                predictions.append(pred)

            df["prediction"] = predictions
            st.success("🎉 Batch prediction completed!")
            st.dataframe(df)

            # Download results as CSV
            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            st.download_button(
                label="⬇️ Download Predictions as CSV",
                data=output,
                file_name="iris_predictions.csv",
                mime="text/csv",
            )

st.markdown("---")
st.caption("Developed by Shivie Saksenaa | MLOps Flask + Streamlit Lab")
