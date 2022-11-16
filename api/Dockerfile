FROM python:3.10-slim

RUN apt-get update && apt-get install make -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
RUN pip install poetry

COPY pyproject.toml /code/
COPY poetry.lock /code/
RUN poetry install

COPY . /code/