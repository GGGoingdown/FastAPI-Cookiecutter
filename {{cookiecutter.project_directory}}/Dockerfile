FROM python:3.9-slim as requirements-stage
WORKDIR /tmp
ARG ENVIRONMENT=PROD
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN if [ "$ENVIRONMENT" = "PROD" ] || [ "$ENVIRONMENT" = "STAG" ] ; then poetry export -f requirements.txt --output requirements.txt --without-hashes ; else poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev; fi

FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    MIGRATION false

WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /app/app
COPY ./script /app/script/
COPY pyproject.tom. .

RUN chmod +x /app/script/service_entrypoint.sh

EXPOSE 8000
