FROM continuumio/miniconda3:latest

LABEL version="1.0" maintainer="Jonathan DEKHTIAR <contact@jonathandekhtiar.eu>"

WORKDIR /app

COPY . /app

RUN pip install --disable-pip-version-check --no-cache-dir -r /app/requirements.txt
