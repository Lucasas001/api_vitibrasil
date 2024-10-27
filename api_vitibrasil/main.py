from fastapi import FastAPI
from api_vitibrasil.api.v1.routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "API is running"}