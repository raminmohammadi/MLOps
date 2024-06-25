from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import flight_router
from fastapi.responses import RedirectResponse
from utils.gcp_model import download_blob
import uvicorn
from dotenv import load_dotenv
from utils.subscribe_bucket_noti import create_subscriber
import asyncio
import threading
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start_subscriber_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_subscriber())

@app.on_event("startup")
async def startup():
    print("Starting up application...")
    download_blob('final-lab-model-bucket', 'models/model.pkl', 'assets/model.pkl')
    download_blob('final-lab-model-bucket', 'models/preprocessorlr.pkl', 'assets/preprocessor.pkl')
    thread = threading.Thread(target=start_subscriber_loop)
    thread.start()
    app.include_router(flight_router.router)

@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")
    files_to_remove = ['assets/model.pkl', 'assets/preprocessor.pkl']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"File {file} removed successfully.")
        else:
            print(f"File {file} does not exist.")

    # os.remove('backend/assets/model.pkl')
    # os.remove('backend/assets/preprocessor.pkl')

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
