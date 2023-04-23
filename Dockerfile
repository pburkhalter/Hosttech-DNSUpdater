# syntax=docker/dockerfile:1
FROM python

MAINTAINER pburkhalter

WORKDIR /app

COPY entrypoint.sh entrypoint.sh
COPY app.py app.py
COPY crontab /etc/cron.d/crontab

RUN apt-get update
RUN apt-get install -y cron python3-requests python3-yaml

RUN chmod +x app.py
RUN chmod +x entrypoint.sh
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

ENTRYPOINT ["/app/entrypoint.sh"]
