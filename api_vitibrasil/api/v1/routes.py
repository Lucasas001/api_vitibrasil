import logging
import datetime
from fastapi import APIRouter, Depends
from api_vitibrasil.services.data_fetcher import fetch_json_data
from api_vitibrasil.services.data_fetcher_ie import fetch_json_data_ie
from api_vitibrasil.services.data_read import CsvRead
from api_vitibrasil.services.verify_credentials import verify_credentials

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
router = APIRouter()

URL_BASE = "http://vitibrasil.cnpuv.embrapa.br"


def fetch_data_with_fallback(
    callback, endpoint: str, csv_filename: str, year: int = None
):
    if year is None:
        year = datetime.datetime.now().year - 1
    url = f"{URL_BASE}/{endpoint}&ano={year}"
    status_code, data = callback(url_base=url)
    if status_code != 200:
        logging.warning("Using alternative route, fetching from CSV")
        data = CsvRead.process_csv(csv_filename, year)
    return {"status_code": status_code, "data": data}


@router.get("/producao/{year}")
@router.get("/producao")
def get_data_producao(year: int = None, username: str = Depends(verify_credentials)):
    """
    Obter dados de produção agrícola para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data, "index.php?opcao=opt_02", "Producao.csv", year
    )


@router.get("/processamento/viniferas/{year}")
@router.get("/processamento/viniferas")
def get_data_processamento_viniferas(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de processamento de uvas viníferas para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data,
        "index.php?opcao=opt_03&subopcao=subopt_01",
        "ProcessaViniferas.csv",
        year,
    )


@router.get("/processamento/americanas_e_hibridas/{year}")
@router.get("/processamento/americanas_e_hibridas")
def get_data_processamento_americanas_hibridas(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de processamento de uvas americanas e híbridas para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data,
        "index.php?opcao=opt_03&subopcao=subopt_02",
        "ProcessaAmericanas.csv",
        year,
    )


@router.get("/processamento/uvas_de_mesa/{year}")
@router.get("/processamento/uvas_de_mesa")
def get_data_processamento_uvas_mesa(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de processamento de uvas de mesa para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data,
        "index.php?opcao=opt_03&subopcao=subopt_03",
        "ProcessaMesa.csv",
        year,
    )


@router.get("/processamento/sem_classificacao/{year}")
@router.get("/processamento/sem_classificacao")
def get_data_processamento_sem_classificacao(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de processamento de uvas sem classificação para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data,
        "index.php?opcao=opt_03&subopcao=subopt_04",
        "ProcessaSemclass.csv",
        year,
    )


@router.get("/comercializacao/{year}")
@router.get("/comercializacao")
def get_data_comercializacao(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de comercialização agrícola para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data, "index.php?opcao=opt_04", "Comercio.csv", year
    )


@router.get("/importacao/vinhos_de_mesa/{year}")
@router.get("/importacao/vinhos_de_mesa")
def get_data_importacao_vinhos_mesa(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de importação de vinhos de mesa para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_01&opcao=opt_05",
        "ImpVinhos.csv",
        year,
    )


@router.get("/importacao/espumantes/{year}")
@router.get("/importacao/espumantes")
def get_data_importacao_espumantes(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de importação de espumantes para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_02&opcao=opt_05",
        "ImpEspumantes.csv",
        year,
    )


@router.get("/importacao/uvas_frescas/{year}")
@router.get("/importacao/uvas_frescas")
def get_data_importacao_uvas_frescas(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de importação de uvas frescas para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_03&opcao=opt_05",
        "ImpFrescas.csv",
        year,
    )


@router.get("/importacao/uvas_passas/{year}")
@router.get("/importacao/uvas_passas")
def get_data_importacao_uvas_passas(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de importação de uvas passas para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_04&opcao=opt_05",
        "ImpPassas.csv",
        year,
    )


@router.get("/importacao/suco_de_uva/{year}")
@router.get("/importacao/suco_de_uva")
def get_data_importacao_suco_uva(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de importação de suco de uva para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_05&opcao=opt_05",
        "ImpSuco.csv",
        year,
    )


@router.get("/exportacao/vinhos_de_mesa/{year}")
@router.get("/exportacao/vinhos_de_mesa")
def get_data_exportacao_vinhos_mesa(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de exportação de vinhos de mesa para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_01&opcao=opt_06",
        "ExpVinho.csv",
        year,
    )


@router.get("/exportacao/espumantes/{year}")
@router.get("/exportacao/espumantes")
def get_data_exportacao_espumantes(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de exportação de espumantes para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_02&opcao=opt_06",
        "ExpEspumantes.csv",
        year,
    )


@router.get("/exportacao/uvas_frescas/{year}")
@router.get("/exportacao/uvas_frescas")
def get_data_exportacao_uvas_frescas(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de exportação de uvas frescas para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_03&opcao=opt_06",
        "ExpUva.csv",
        year,
    )


@router.get("/exportacao/suco_de_uva/{year}")
@router.get("/exportacao/suco_de_uva")
def get_data_exportacao_suco_uva(
    year: int = None, username: str = Depends(verify_credentials)
):
    """
    Obter dados de exportação de suco de uva para o ano especificado.
    - **year**: Ano de referência (opcional). Se não especificado, utiliza o ano anterior.
    """
    return fetch_data_with_fallback(
        fetch_json_data_ie,
        "index.php?subopcao=subopt_04&opcao=opt_06",
        "ExpSuco.csv",
        year,
    )
