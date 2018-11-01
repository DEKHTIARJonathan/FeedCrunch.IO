FROM continuumio/miniconda3:latest

LABEL version="1.0" maintainer="Jonathan DEKHTIAR <contact@jonathandekhtiar.eu>"

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get install -y git vim wget curl \
    && pip install --disable-pip-version-check --no-cache-dir --upgrade -r /app/requirements.txt \
    && pip install --disable-pip-version-check --no-cache-dir --upgrade -r /app/requirements_test.txt \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
