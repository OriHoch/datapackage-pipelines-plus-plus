FROM python:3.6-alpine

# install system requirements
RUN apk add --update --no-cache --virtual=build-dependencies \
    build-base \
    curl \
    jpeg-dev \
    libxml2-dev libxml2 \
    libxslt-dev libxslt \
    libstdc++ \
    libpq \
    python3-dev postgresql-dev
RUN apk --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --update add leveldb leveldb-dev
RUN pip install psycopg2 datapackage-pipelines-github lxml datapackage-pipelines[speedup]
RUN apk add --update --no-cache git

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

RUN mkdir /pipelines
WORKDIR /pipelines
COPY . /pipelines/

ENV PYTHONUNBUFFERED 1

RUN cd /pipelines && pip install .

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 5000
VOLUME /pipelines
