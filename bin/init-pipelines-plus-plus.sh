#!/usr/bin/env bash

GITHUB_REPO="OriHoch/datapackage-pipelines-plus-plus"
BRANCH="master"
BASEURL="https://raw.githubusercontent.com/${GITHUB_REPO}/${BRANCH}"
BASENAME=`basename $PWD`

function copy() {
    curl "${BASEURL}/${1}" > "${1}"
}

if [ "${BASENAME}" != "datapackage-pipelines-plus-plus" ]; then
    # this initiates a new pipelines plus plus project in a different directory
    # it copies the latest files from github master
    mkdir -p bin
    copy bin/start.sh
    copy bin/init-pipelines-plus-plus.sh
    copy bin/update_compose.sh
    copy bin/dpp.sh
    copy docker-compose.override.example.yml
    copy docker-compose.yml

    chmod +x bin/*.sh
fi

bin/update_compose.sh
