from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    Defines the root endpoint for the FastAPI application.

    This endpoint responds to GET requests at the root URL ("/") and returns
    a JSON object containing a greeting message.

    Returns:
        dict: A dictionary with a key "message" and a value "Hello World GKE".
    """
    return {"message": "Hello World GKE"}