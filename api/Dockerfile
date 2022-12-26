FROM python:3.10-slim

RUN apt update &&\
    apt install gprolog python3-pip git -y
RUN git clone https://github.com/m-danya/prolog-testing-system &&\
    cd prolog-testing-system/api &&\
    pip install -r requirements.txt &&\
    pip install gunicorn uwsgi

EXPOSE 3001
CMD cd prolog-testing-system/api && mkdir submissions && gunicorn --bind 0.0.0.0:3001 wsgi:app run