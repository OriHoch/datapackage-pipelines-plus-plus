# Datapackage Pipelines Plus Plus

Enhance the datapackage-pipelines framework with some more opinionated architecture and easy to use code


## Features

* Object oriented processors - allows for extensibility and code re-use.
* Docker compose stack - allows for a complex architecture which is easy to setup and ensured to be the same across environments.

## Usage

### Quickstart

The common usage is to start a new code repository which will use the pipelines plus plus framework.

First, make sure you install Docker and Docker Compose - refer to Docker documentation for details.

Run the following command from within the new project directory:

* `source <(curl -s https://raw.githubusercontent.com/OriHoch/datapackage-pipelines-plus-plus/master/bin/init-pipelines-plus-plus.sh)`

You can start the docker compose services by running:

* `bin/start.sh`

By default it provides the following services:

* Pipelines Dashboard - http://localhost:5000
* Kibana - http://localhost:15601
* Elasticsearch - http://localhost:19200
* PostgreSQL - postgresql://postgres:123456@datadb:5432/postgres
* Adminer (DB admin web ui) - http://localhost:18080
