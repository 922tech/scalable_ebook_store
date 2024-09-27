
FROM python:3.10-slim AS python_mid

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /wheels

COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /requirements.txt


FROM python:3.10-slim

COPY --from=python_mid /wheels /wheels
RUN pip install --no-cache /wheels/*

WORKDIR /ebook_store
RUN mkdir /ebook_store/static
COPY . .
