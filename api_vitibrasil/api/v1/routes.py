import logging
from fastapi import APIRouter
from api_vitibrasil.services.data_fetcher import fetch_json_data
from api_vitibrasil.services.data_fetcher_ie import fetch_json_data_ie


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
router = APIRouter()

URL_BASE = "http://vitibrasil.cnpuv.embrapa.br"
@router.get("/producao/{year}")
@router.get("/producao")
def get_data_viniferas(year: int = None):
    url = f"{URL_BASE}/index.php?opcao=opt_02"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data(url_base=url)
    return {"status_code": status_code, "data": data}


@router.get("/processamento/viniferas/{year}")
@router.get("/processamento/viniferas")
def get_data_viniferas(year: int = None):
    url = f"{URL_BASE}/index.php?opcao=opt_03&subopcao=subopt_01"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data(url_base=url)
    return {"status_code": status_code, "data": data}


@router.get("/processamento/americanas_e_hibridas/{year}")
@router.get("/processamento/americanas_e_hibridas")
def get_data_americanas_hibridas(year: int = None):
    url = f"{URL_BASE}/index.php?opcao=opt_03&subopcao=subopt_02"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data(url_base=url)
    return {"status_code": status_code, "data": data}


@router.get("/processamento/uvas_de_mesa/{year}")
@router.get("/processamento/uvas_de_mesa")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?opcao=opt_03&subopcao=subopt_03"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data(url_base=url)
    return {"status_code": status_code, "data": data}


@router.get("/comercializacao/{year}")
@router.get("/comercializacao/")
def get_data(year: int = None):

    url = f"{URL_BASE}/index.php?opcao=opt_04"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/importacao/vinhos_de_mesa/{year}")
@router.get("/importacao/vinhos_de_mesa")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_01&opcao=opt_05"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}


@router.get("/importacao/espumantes/{year}")
@router.get("/importacao/espumantes")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_02&opcao=opt_05"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/importacao/uvas_frescas/{year}")
@router.get("/importacao/uvas_frescas")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_03&opcao=opt_05"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/importacao/uvas_passas/{year}")
@router.get("/importacao/uvas_passas")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_04&opcao=opt_05"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/importacao/suco_de_uva/{year}")
@router.get("/importacao/suco_de_uva")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_05&opcao=opt_05"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}


# Export
@router.get("/exportacao/vinhos_de_mesa/{year}")
@router.get("/exportacao/vinhos_de_mesa")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_01&opcao=opt_06"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/exportacao/espumantes/{year}")
@router.get("/exportacao/espumantes")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_02&opcao=opt_06"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/exportacao/uvas_frescas/{year}")
@router.get("/exportacao/uvas_frescas")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_03&opcao=opt_06"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}

@router.get("/exportacao/suco_de_uva/{year}")
@router.get("/exportacao/suco_de_uva")
def get_data(year: int = None):
    url = f"{URL_BASE}/index.php?subopcao=subopt_04&opcao=opt_06"
    if year:
        url += f"&ano={year}"

    status_code, data = fetch_json_data_ie(url_base=url)
    return {"status_code": status_code, "data": data}



