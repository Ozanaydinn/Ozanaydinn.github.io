FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt \
    && apt-get clean \
    && apt-get -y update \
    && apt-get -y install \
    ffmpeg \
    libsm6 \
    libxext6

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
