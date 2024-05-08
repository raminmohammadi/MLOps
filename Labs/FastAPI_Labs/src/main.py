from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel
from predict import predict_data
import uvicorn


app = FastAPI()

class IrisData(BaseModel):
    petal_length: float
    sepal_length:float
    petal_width:float
    sepal_width:float

class IrisResponse(BaseModel):
    response:int

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

# @app.post("/predict", response_model=IrisResponse)
# async def predict_iris(iris_features: IrisData):
#     try:
#         features = [[iris_features.sepal_length, iris_features.sepal_width,
#                     iris_features.petal_length, iris_features.petal_width]]

#         prediction = predict_data(features)
#         return IrisResponse(response=int(prediction[0]))
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.route("/predict", methods=["GET", "POST"], response_model=IrisResponse)
async def predict_iris(iris_features: IrisData):
    if Request.method == "POST":
        try:
            features = [[iris_features.sepal_length, iris_features.sepal_width,
                        iris_features.petal_length, iris_features.petal_width]]

            prediction = predict_data(features)
            return IrisResponse(response=int(prediction[0]))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    elif Request.method == "GET":
        # Handle GET request (if needed)
        return {"message": "GET request received"}

    
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
    



    
