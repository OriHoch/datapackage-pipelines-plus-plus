#!/usr/bin/env bash

if [ -f "docker-compose.override.yml" ]; then
    echo "replacing existing docker-compose.override.yml file"
    echo "creating backup copy at docker-compose.override.yml.bak"
    mv docker-compose.override.yml docker-compose.override.yml.bak
fi

cp docker-compose.override.example.yml docker-compose.override.yml
