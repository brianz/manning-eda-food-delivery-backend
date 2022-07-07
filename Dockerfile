FROM python:3.9

RUN apt-get update && \
    apt install -y iputils-ping dnsutils

RUN pip install -U \
    pip \
    pipenv

ADD . /code
WORKDIR /code

ARG ENV=production
RUN make pipenv