#!/usr/bin/env bash

docker-compose build pipelines
docker push orihoch/datapackage-pipelines-plus-plus
