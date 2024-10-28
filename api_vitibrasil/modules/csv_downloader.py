import os
import requests
from typing import List
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CsvDownloader:
    def __init__(
        self,
        base_url: str,
        files: List[str],
        download_dir: str = "api_vitibrasil/csv/csv_raw",
    ):
        self.base_url = base_url
        self.files = files
        self.download_dir = download_dir
        # Cria o diretório se ele não existir
        os.makedirs(self.download_dir, exist_ok=True)

    def download_file(self, file_name: str):
        url = self.base_url + file_name
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                file_path = os.path.join(self.download_dir, file_name)
                with open(file_path, "wb") as file:
                    file.write(response.content)
                logging.info(f"Arquivo {file_path} baixado com sucesso.")
        except requests.exceptions.RequestException:
            logging.error(f"Arquivo {file_name} indisponível")

    def download_all_files(self):
        for file in self.files:
            self.download_file(file)


if __name__ == "__main__":
    base_url = "http://vitibrasil.cnpuv.embrapa.br/download/"
    files = [
        "Producao.csv",
        "ProcessaViniferas.csv",
        "ProcessaAmericanas.csv",
        "ProcessaMesa.csv",
        "ProcessaSemclass.csv",
        "Comercio.csv",
        "ImpVinhos.csv",
        "ImpEspumantes.csv",
        "ImpFrescas.csv",
        "ImpPassas.csv",
        "ImpSuco.csv",
        "ExpVinho.csv",
        "ExpEspumantes.csv",
        "ExpUva.csv",
        "ExpSuco.csv",
    ]

    # Instancia a classe e baixa os arquivos
    downloader = CsvDownloader(base_url, files)
    downloader.download_all_files()
