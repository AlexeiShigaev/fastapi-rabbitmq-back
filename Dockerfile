FROM python:3.11.7-alpine

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip poetry
RUN poetry config virtualenvs.create false --local
#RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry install
