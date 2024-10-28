import pandas as pd
import os
from typing import Dict, Any


class CsvRead:
    def __init__(
        self,
        csv_name: str,
        year: int,
        base_path: str = "api_vitibrasil/csv/csv_refined",
    ):
        # Monta o caminho do arquivo com base no nome do CSV
        self.file_path = os.path.join(base_path, csv_name)
        self.year = year
        self.df = None

    def load_csv(self):
        # Carrega o arquivo CSV com ';' como delimitador
        self.df = pd.read_csv(self.file_path, sep=";")

    def filter_by_year(self):
        # Verifica se a coluna 'ano' existe e filtra o DataFrame
        if "ano" in self.df.columns:
            self.df = self.df[self.df["ano"] == self.year].copy()
        else:
            raise ValueError(f"Coluna 'ano' não encontrada no arquivo {self.file_path}")

    def to_json(self) -> Dict[str, Any]:
        # Converte o DataFrame formatado para o formato de dicionário JSON
        json_data_dict = {"data": self.df.to_dict(orient="records")}
        return json_data_dict

    def process(self) -> Dict[str, Any]:
        # Carrega e processa o CSV em uma única função
        self.load_csv()
        self.filter_by_year()
        return self.to_json()

    def process_csv(csv_name: str, year: int):
        processor = CsvRead(csv_name, year)
        return processor.process()
