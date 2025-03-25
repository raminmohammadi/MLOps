'''
This module defines a FastAPI application with a single endpoint to perform addition of two integers.

Modules:
- fastapi: The FastAPI framework for building APIs.
- fastapi.middleware.cors: Middleware to handle Cross-Origin Resource Sharing (CORS).

Application:
- The FastAPI application is configured with CORS middleware to allow requests from any origin.

Endpoints:
- /add (GET): Adds two integers provided as query parameters.

Functions:
- add(a: int, b: int) -> dict:
'''

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # Allows requests from any origin (public access)
    allow_methods=["*"],          # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],          # Allows all headers in incoming requests
)

@app.get("/add")
async def add(a: int = Query(..., description="The first number"), 
              b: int = Query(..., description="The second number")):
    """
    Endpoint to add two integers.

    Query Parameters:
    - a (int): The first number to be added. This is a required parameter.
    - b (int): The second number to be added. This is a required parameter.

    Returns:
    - dict: A dictionary containing the sum of the two numbers with the key "sum".
    """
    return {"sum": a + b}