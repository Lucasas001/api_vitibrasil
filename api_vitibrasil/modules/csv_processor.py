import os
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CsvProcessor:
    def __init__(self, csv_name: str, csv_type: str):
        self.csv_name = csv_name
        self.csv_type = csv_type
        self.df = None
        self.file_path = os.path.join("api_vitibrasil/csv/csv_raw", csv_name)
        self.output_folder = "api_vitibrasil/csv/csv_refined"

    def load_csv(self):
        # Tenta carregar com ';'
        self.df = pd.read_csv(self.file_path, sep=";")

        if len(self.df.columns) == 1:
            self.df = pd.read_csv(self.file_path, sep="\t")

    @staticmethod
    def fill_item_column_from_produto(
        df: pd.DataFrame, subitem_column: str
    ) -> List[str]:
        current_item = None
        item_column = []
        for produto_value in df[subitem_column]:
            if isinstance(produto_value, str) and produto_value.isupper():
                current_item = produto_value
            item_column.append(current_item)
        return item_column

    def process_tipo_1(self):
        self.load_csv()
        if "id" in self.df.columns and "control" in self.df.columns:
            self.df.drop(columns=["id", "control"], inplace=True)

        if "Produto" in self.df.columns or "produto" in self.df.columns:
            self.df.rename(
                columns={"Produto": "subitem", "produto": "subitem"}, inplace=True
            )

        if "subitem" in self.df.columns:
            self.df["item"] = self.fill_item_column_from_produto(self.df, "subitem")
            self.reorder_columns()
            self.unpivot_data()
        else:
            logging.error(f"'subitem' column not found in {self.csv_name}")
        return self.df

    def process_tipo_2(self):
        self.load_csv()
        if "id" in self.df.columns and "control" in self.df.columns:
            self.df.drop(columns=["id", "control"], inplace=True)

        if "cultivar" in self.df.columns:
            self.df.rename(columns={"cultivar": "subitem"}, inplace=True)

        if "subitem" in self.df.columns:
            self.df["item"] = self.fill_item_column_from_produto(self.df, "subitem")
            self.reorder_columns()
            self.unpivot_data()
        else:
            logging.error(f"'subitem' column not found in {self.csv_name}")
        return self.df

    def process_tipo_3(self):
        self.load_csv()
        kg_cols = [
            col
            for col in self.df.columns
            if not ".1" in col and col not in ["Id", "País"]
        ]
        valor_cols = [col for col in self.df.columns if ".1" in col]
        valor_cols_renamed = [col.replace(".1", "") for col in valor_cols]

        df_kg = self.df[["Id", "País"] + kg_cols].copy()
        df_valor = self.df[["Id", "País"] + valor_cols].copy()
        df_valor.columns = ["Id", "País"] + valor_cols_renamed

        df_kg_melted = df_kg.melt(
            id_vars=["Id", "País"], var_name="Ano", value_name="kg"
        )
        df_valor_melted = df_valor.melt(
            id_vars=["Id", "País"], var_name="Ano", value_name="valor"
        )

        df_final = pd.merge(df_kg_melted, df_valor_melted, on=["Id", "País", "Ano"])
        self.df = df_final[["País", "Ano", "kg", "valor"]].copy()

        if "País" in self.df.columns:
            self.df.rename(
                columns={
                    "País": "paises",
                    "Ano": "ano",
                    "kg": "quantidade_kg",
                    "valor": "valor_us",
                },
                inplace=True,
            )

        return self.df

    def reorder_columns(self):
        cols = ["item"] + [col for col in self.df.columns if col != "item"]
        self.df = self.df[cols].copy()

    def unpivot_data(self):
        year_columns = [col for col in self.df.columns if col.isdigit()]
        self.df = pd.melt(
            self.df,
            id_vars=["item", "subitem"],
            value_vars=year_columns,
            var_name="ano",
            value_name="valor",
        ).copy()

    def save_to_csv(self):
        # Cria a pasta de saída se ela não existir
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Define o caminho completo para salvar o CSV
        output_path = os.path.join(self.output_folder, self.csv_name)
        self.df.to_csv(output_path, index=False, sep=";")
        logging.info(f"Arquivo normalizados salvo em: {output_path}")


def process_csv_files(csv_types: List[Dict[str, str]]):
    for entry in csv_types:
        for csv_name, csv_type in entry.items():
            processor = CsvProcessor(csv_name, csv_type)
            if csv_type == "tipo_1":
                processor.process_tipo_1()
            elif csv_type == "tipo_2":
                processor.process_tipo_2()
            elif csv_type == "tipo_3":
                processor.process_tipo_3()
            processor.save_to_csv()


# Processar os arquivos CSV e salvá-los em csv_normalized
if __name__ == "__main__":
    # Arquivos e tipos de processamento
    csv_types = [
        {"Comercio.csv": "tipo_1"},
        {"Producao.csv": "tipo_1"},
        {"ProcessaAmericanas.csv": "tipo_2"},
        {"ProcessaMesa.csv": "tipo_2"},
        {"ProcessaSemclass.csv": "tipo_2"},
        {"ProcessaViniferas.csv": "tipo_2"},
        {"ImpVinhos.csv": "tipo_3"},
        {"ImpEspumantes.csv": "tipo_3"},
        {"ImpFrescas.csv": "tipo_3"},
        {"ImpPassas.csv": "tipo_3"},
        {"ImpSuco.csv": "tipo_3"},
        {"ExpVinho.csv": "tipo_3"},
        {"ExpEspumantes.csv": "tipo_3"},
        {"ExpUva.csv": "tipo_3"},
        {"ExpSuco.csv": "tipo_3"},
    ]
    process_csv_files(csv_types)
