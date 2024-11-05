from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import uvicorn

app = FastAPI()

# Load IMDb dataset
data = pd.read_csv('IMDb_Reviews.csv')

# Preprocess data
X = data['review']
y = data['sentiment']

 # Vectorize text data
vectorizer = TfidfVectorizer(max_features=5000)
X_train = vectorizer.fit_transform(X)
model = LogisticRegression()
model.fit(X_train, y)

class Review(BaseModel):
    review: str

@app.post("/predict/")
def predict_sentiment(review: Review):
    X_new = vectorizer.transform([review.review])
    prediction = model.predict(X_new)
    return {"sentiment": prediction[0]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)