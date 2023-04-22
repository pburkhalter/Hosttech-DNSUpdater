# syntax=docker/dockerfile:1
FROM python

MAINTAINER pburkhalter

WORKDIR /app

RUN apt-get update
RUN apt-get install -y cron python3-requests python3-yaml

COPY entrypoint.sh entrypoint.sh
COPY app.py app.py
COPY cronjob /etc/cron.d/hosttech-updater

RUN crontab /etc/cron.d/hosttech-updater

ENTRYPOINT ["cron", "-f"]


