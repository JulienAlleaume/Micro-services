FROM python:3.11

WORKDIR /app

# Installation des dépendances
RUN pip install fastapi uvicorn sqlalchemy pydantic pika

COPY . .
