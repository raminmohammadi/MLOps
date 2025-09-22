from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from predict import predict_data

app = FastAPI(title="Diabetes Prediction API")

class DiabetesData(BaseModel):
    Pregnancies: int 
    Glucose: float  
    BloodPressure: float 
    SkinThickness: float 
    Insulin: float  
    BMI: float 
    DiabetesPedigreeFunction: float 
    Age: int 
    

class PredictionResponse(BaseModel):
    response: int

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_diabetes(data: DiabetesData):
    try:
        features = [
            data.Pregnancies,
            data.Glucose,
            data.BloodPressure,
            data.SkinThickness,
            data.Insulin,
            data.BMI,
            data.DiabetesPedigreeFunction,
            data.Age
        ]
        prediction = predict_data(features)
        return PredictionResponse(response=int(prediction[0]))
    except FileNotFoundError as e:
        # Model not trained yet
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

