FROM python:3.11.9-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_SYSTEM_PYTHON=1


WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

ADD alembic.ini /app

RUN pip install --upgrade pip

COPY ./pyproject.toml ./uv.lock /app/
RUN uv pip install -r pyproject.toml


COPY /src/* /app/src/
COPY /tests/* /app/tests/