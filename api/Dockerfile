FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN apt update &&\
    apt install gprolog python3-pip -y &&\
    pip install -r requirements.txt &&\
    pip install gunicorn uwsgi

EXPOSE 3001
CMD gunicorn --bind 0.0.0.0:3001 --certfile=server.crt --keyfile=server.key wsgi:app run