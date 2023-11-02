FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

# update apt and install gcc with python3-dev
RUN apk update && apk add --no-cache gcc python3-dev musl-dev bash

EXPOSE 8000

WORKDIR /app

COPY pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY ./src .
