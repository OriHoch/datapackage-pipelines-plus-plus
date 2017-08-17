#!/usr/bin/env bash

mkdir -p .docker-data/pipelines

docker-compose up -d --build
