# Função para carregar cada CSV para o Redis
def load_csv_to_redis(csv_directory):
    # Itera sobre todos os arquivos CSV na pasta especificada
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)
            table_name = os.path.splitext(filename)[
                0
            ]  # Usa o nome do arquivo sem extensão como a chave

            with open(file_path, mode="r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file, delimiter=";")
                headers = csv_reader.fieldnames  # Obter os nomes dos campos
                print(
                    f"Cabeçalhos do arquivo '{filename}': {headers}"
                )  # Verificar os cabeçalhos

                for row in csv_reader:
                    print(f"Lendo linha: {row}")  # Depurar o conteúdo da linha
                    if "id" in row and "control" in row:
                        key = f"{table_name}:{row['id']}_{row['control']}"  # Cria uma chave única por 'id' e 'control'

                        # Criar um dicionário com o Produto e os anos (1970 até 2023)
                        data = {
                            "Produto": row["Produto"],
                            **{
                                year: row[year] for year in row if year.isdigit()
                            },  # Mapeia os anos e seus valores
                        }

                        # Usar hset em vez de hmset
                        r.hset(key, mapping=data)
                    else:
                        print(
                            f"Erro: A linha não contém 'id' ou 'control' no arquivo '{filename}'."
                        )


# Caminho para a pasta CSV
csv_directory = "./csv"

# Executa o carregamento dos CSVs para o Redis
load_csv_to_redis(csv_directory)
print("Todos os CSVs foram carregados no Redis com sucesso!")
