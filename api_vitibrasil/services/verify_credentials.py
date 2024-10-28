import os
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


protected_routes = APIRouter()
security = HTTPBasic()

# Carregar as credenciais de variáveis de ambiente
USERNAME = os.getenv("BASIC_AUTH_USERNAME", "fiap")
PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "FIAP123")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
