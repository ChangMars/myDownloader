FROM python:3.8.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /mydownloader
WORKDIR /mydownloader
COPY . /mydownloader

RUN pip install -r requirements.txt

RUN    apt-get update \
    && apt-get install openssl \
    && apt-get install ca-certificates