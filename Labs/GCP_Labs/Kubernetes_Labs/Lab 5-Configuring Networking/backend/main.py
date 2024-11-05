from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/add")
async def add(a: int = Query(..., description="The first number"), 
              b: int = Query(..., description="The second number")):
    return {"sum": a + b}
