#!/usr/bin/env bash

docker build -t orihoch/datapackage-pipelines-plus-plus-elasticsearch elasticsearch
docker build -t orihoch/datapackage-pipelines-plus-plus-kibana kibana
docker push orihoch/datapackage-pipelines-plus-plus-elasticsearch
docker push orihoch/datapackage-pipelines-plus-plus-kibana
