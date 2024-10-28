FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y cron
RUN chmod +x entrypoint.sh
COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job
RUN touch /var/log/cron.log

ENTRYPOINT ["/bin/sh","entrypoint.sh"]