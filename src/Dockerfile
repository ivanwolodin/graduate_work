FROM tiangolo/uvicorn-gunicorn:python3.10

ARG DB_CONNECTION
ARG MODE

ENV SQLALCHEMY_DATABASE_URI=${DB_CONNECTION}
ENV MODE=${MODE}

COPY ./requirements.txt .
RUN pip install -r base.txt

COPY ./scripts /app
COPY ./recsys_api /app
WORKDIR /app
