FROM python:3.11-slim

# Installation de uv via pip
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copie du manifeste en premier pour profiter du cache des layers Docker
COPY pyproject.toml .

# Installation des dependances sans installer le projet lui-meme
RUN uv sync --no-install-project

COPY . .
