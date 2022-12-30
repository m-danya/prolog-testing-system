FROM python:3

WORKDIR /app
COPY . /app

RUN apt update &&\
    apt install gprolog -y &&\
    pip install -r requirements.txt &&\
    pip install gunicorn uwsgi

EXPOSE ${BACKEND_PORT}
CMD gunicorn --bind 0.0.0.0:${BACKEND_PORT} --certfile=${SSL_CRT_FILE} --keyfile=${SSL_KEY_FILE} wsgi:app run
