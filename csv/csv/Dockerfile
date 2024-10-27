# Usa uma imagem Python como base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala o SQLite no sistema
RUN apt-get update && apt-get install -y sqlite3

# Mantém o container ativo com o SQLite
CMD ["sqlite3"]
