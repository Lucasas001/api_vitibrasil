#!/bin/sh

# Inicia o cron em segundo plano
cron && tail -f /var/log/cron.log &
echo "Executa o script csv_downloader.py na inicialização"
poetry run python3 /app/api_vitibrasil/modules/csv_downloader.py
echo "Executa o script csv_processor.py na inicialização"
poetry run python3 /app/api_vitibrasil/modules/csv_processor.py
echo "Scripts finalizados, iniciando API Service"
poetry run start