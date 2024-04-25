FROM python:3.11

WORKDIR /src

COPY requirements.txt .

RUN apt-get update && \
    pip install -r requirements.txt --no-cache-dir

COPY .. .

CMD ["python", "./main.py"]


# FROM python:3.11
#
# #ARG DB_CONNECTION
# #ARG MODE
#
# #ENV SQLALCHEMY_DATABASE_URI=${DB_CONNECTION}
# #ENV MODE=${MODE}
#
# COPY /recsys_api/requirements.txt .
# RUN pip install -r requirements.txt
#
# #COPY ./scripts /app
# COPY ./recsys_api /app


#WORKDIR /app

#CMD nohup python main.py
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
# WORKDIR /src/recsys_api
#
#
# COPY requirements.txt .
#
# RUN apt-get update && \
#     pip install -r requirements.txt --no-cache-dir
#
# COPY .. .

# CMD ["python", "main.py"]