
import uvicorn

def main():
    uvicorn.run("api_vitibrasil.main:app", host="0.0.0.0", port=8000, reload=True)