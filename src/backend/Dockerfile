FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt \
     && pip3 install https://github.com/mher/flower/zipball/master

COPY . .
