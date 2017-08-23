#!/usr/bin/env bash

GITHUB_REPO="OriHoch/datapackage-pipelines-plus-plus"
BRANCH="master"
BASEURL="https://raw.githubusercontent.com/${GITHUB_REPO}/${BRANCH}"
BASENAME=`basename $PWD`

function copy() {
    echo "${BASEURL}/${1} > ${1}"
    curl "${BASEURL}/${1}" > "${1}"
}

if [ "${BASENAME}" != "datapackage-pipelines-plus-plus" ]; then
    # this initiates a new pipelines plus plus project in a different directory
    # it copies the latest files from github master
    #
    # it will overwrite any existing files, but all these files are supposed to be in Git

    mkdir -p bin
    copy bin/dpp.sh
    copy bin/init-pipelines-plus-plus.sh
    copy bin/install.sh
    copy bin/start.sh
    chmod +x bin/*.sh

    copy .env.example
    copy .gitignore
    copy docker-compose.override.example.yml
    copy docker-compose.yml
    copy plus_plus.source-spec.yaml
    copy plus_plus.source-spec.override.example.yaml
    copy requirements.txt
    copy README.md
    echo "-e git+https://github.com/OriHoch/datapackage-pipelines-plus-plus.git#egg=datapackage_pipelines_plus_plus[develop]" >> requirements.txt
    if [ ! -f docker-compose.override.yml ]; then
        # this is the only file we don't overwrite - because it's not committed to git
        cp docker-compose.override.example.yml docker-compose.override.yml
    fi
fi
