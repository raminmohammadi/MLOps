from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from schemas.flight_request import FlightData
from schemas.prediction_response import DelayedResponse
# import random
import pickle
import numpy as np
import pandas as pd

router = APIRouter(prefix='/flight', tags=['Flight prediction'])

def add_date_features(df):
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
    df['MONTH'] = df['FL_DATE'].dt.month
    df['WEEKDAY'] = df['FL_DATE'].dt.weekday
    df['DAY'] = df['FL_DATE'].dt.day
    return df

@router.post("/prediction", status_code=status.HTTP_200_OK, response_model=DelayedResponse)
def get_flight_delays(request: FlightData):

    try:
        
        with open('assets/preprocessor.pkl', 'rb') as preprocessor_file:
            preprocessor = pickle.load(preprocessor_file)

        with open('assets/model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)

        input_data = pd.DataFrame([request.dict()])
        input_data = add_date_features(input_data)
        
        processed_features = preprocessor.transform(input_data)
        
        prediction = model.predict(processed_features)
        is_delayed = bool(prediction[0])
        
        return DelayedResponse(
            success=True,
            delayed=is_delayed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # delayed = random.choice([True, False])
    # return DelayedResponse(
    #     success=True,
    #     delayed=delayed
    # )
