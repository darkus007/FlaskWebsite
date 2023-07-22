# syntax=docker/dockerfile:1
FROM python:3.11.1-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY src /website/src
COPY migrations /website/migrations
COPY alembic.ini /website
COPY config.py /website

WORKDIR /website
EXPOSE 8000

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY ./entrypoint.sh /website
ENTRYPOINT ["/website/entrypoint.sh"]
