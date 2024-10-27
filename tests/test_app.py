from fastapi.testclient import TestClient
from api_vitibrasil.app import app


def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de consulta da EMBRAPA"}
