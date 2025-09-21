from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_dt, predict_rf, predict_lr

app = FastAPI()

# Map class indices to species names
CLASS_MAP = {0: "setosa", 1: "versicolor", 2: "virginica"}


class IrisData(BaseModel):
    """Request schema for iris flower features."""

    petal_length: float
    sepal_length: float
    petal_width: float
    sepal_width: float


class IrisResponse(BaseModel):
    """Response schema with both numeric label and species name."""

    response: int
    species: str


@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    """Health check endpoint."""
    return {"status": "healthy"}


# ---- Decision Tree ----
@app.post("/predict/dt", response_model=IrisResponse)
async def predict_iris_dt(iris_features: IrisData):
    """Predict species using Decision Tree classifier."""
    try:
        features = [
            [
                iris_features.sepal_length,
                iris_features.sepal_width,
                iris_features.petal_length,
                iris_features.petal_width,
            ]
        ]
        prediction = int(predict_dt(features)[0])
        return IrisResponse(response=prediction, species=CLASS_MAP[prediction])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Random Forest ----
@app.post("/predict/rf", response_model=IrisResponse)
async def predict_iris_rf(iris_features: IrisData):
    """Predict species using Random Forest classifier."""
    try:
        features = [
            [
                iris_features.sepal_length,
                iris_features.sepal_width,
                iris_features.petal_length,
                iris_features.petal_width,
            ]
        ]
        prediction = int(predict_rf(features)[0])
        return IrisResponse(response=prediction, species=CLASS_MAP[prediction])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Logistic Regression ----
@app.post("/predict/lr", response_model=IrisResponse)
async def predict_iris_lr(iris_features: IrisData):
    """Predict species using Logistic Regression model."""
    try:
        features = [
            [
                iris_features.sepal_length,
                iris_features.sepal_width,
                iris_features.petal_length,
                iris_features.petal_width,
            ]
        ]
        prediction = int(predict_lr(features)[0])
        return IrisResponse(response=prediction, species=CLASS_MAP[prediction])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
