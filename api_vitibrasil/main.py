from fastapi import FastAPI
from api_vitibrasil.api.v1.routes import router

app = FastAPI(
    title="API VitiBrasil",
    description="API criada para atividade do Tech Challenge FIAP, pelos alunos Lucas Araujo (RM358757) e Lucas Martins (RM358914)",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "API is running..."}
