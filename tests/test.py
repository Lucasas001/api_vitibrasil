from fastapi.testclient import TestClient
from api_vitibrasil.main import app
from http import HTTPStatus
from unittest.mock import patch
import base64

client = TestClient(app)


# Função auxiliar para gerar o cabeçalho de autenticação
def get_auth_header(username: str, password: str) -> dict:
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


auth_header = get_auth_header("fiap", "FIAP123")

# Rotas para testar
routes = [
    "/producao",
    "/producao/2023",
    "/processamento/viniferas",
    "/processamento/viniferas/2023",
    "/processamento/americanas_e_hibridas",
    "/processamento/americanas_e_hibridas/2023",
    "/processamento/uvas_de_mesa",
    "/processamento/uvas_de_mesa/2023",
    "/processamento/sem_classificacao",
    "/processamento/sem_classificacao/2023",
    "/comercializacao",
    "/comercializacao/2023",
    "/importacao/vinhos_de_mesa",
    "/importacao/vinhos_de_mesa/2023",
    "/importacao/espumantes",
    "/importacao/espumantes/2023",
    "/importacao/uvas_frescas",
    "/importacao/uvas_frescas/2023",
    "/importacao/uvas_passas",
    "/importacao/uvas_passas/2023",
    "/importacao/suco_de_uva",
    "/importacao/suco_de_uva/2023",
    "/exportacao/vinhos_de_mesa",
    "/exportacao/vinhos_de_mesa/2023",
    "/exportacao/espumantes",
    "/exportacao/espumantes/2023",
    "/exportacao/uvas_frescas",
    "/exportacao/uvas_frescas/2023",
    "/exportacao/suco_de_uva",
    "/exportacao/suco_de_uva/2023",
]


# Testes para todas as rotas usando um loop
def test_routes():
    for route in routes:
        with patch(
            "api_vitibrasil.services.data_fetcher.fetch_json_data"
        ) as mock_fetch:
            mock_fetch.return_value = (
                200,
                [{"item": "Example", "subitem": "Example", "value": "12345"}],
            )
            response = client.get(route, headers=auth_header)
            assert response.status_code == HTTPStatus.OK
            assert "data" in response.json()
            assert isinstance(response.json()["data"], list)


# Teste de fallback para CSV em todas as rotas
def test_routes_fallback_to_csv():
    for route in routes:
        with patch(
            "api_vitibrasil.services.data_fetcher.fetch_json_data"
        ) as mock_fetch, patch(
            "api_vitibrasil.services.data_read.CsvRead.process_csv"
        ) as mock_csv:

            mock_fetch.return_value = (500, None)  # Simula falha na requisição
            mock_csv.return_value = [
                {"item": "Example CSV", "subitem": "Example CSV", "value": "12345"}
            ]

            response = client.get(route, headers=auth_header)
            assert response.status_code == HTTPStatus.OK
            assert "data" in response.json()
            assert isinstance(response.json()["data"], list)
