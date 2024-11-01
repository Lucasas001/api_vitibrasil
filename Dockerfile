FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN apt-get update && \
    apt-get install -y cron && \
    chmod +x entrypoint.sh && \
    cp crontab /etc/cron.d/my-cron-job && \
    chmod 0644 /etc/cron.d/my-cron-job && \
    crontab /etc/cron.d/my-cron-job && \
    touch /var/log/cron.log

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]
