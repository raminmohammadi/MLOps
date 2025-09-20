from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data
import numpy as np
import joblib


app = FastAPI()

class PenguinData(BaseModel):
    bill_length: float
    bill_depth: float
    flipper_length: float
    body_mass: float

class PenguinResponse(BaseModel):
    response:str


@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=PenguinResponse)
async def predict_penguin(penguin_features: PenguinData):
    try:
        art = joblib.load("../model/penguin_artifact.joblib")
        classes = art["classes"]

        features = [[penguin_features.bill_length, penguin_features.bill_depth,
                    penguin_features.flipper_length, penguin_features.body_mass]]

        prediction = predict_data(np.array(features, dtype=float))
        return PenguinResponse(response=classes[int(prediction[0])])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
