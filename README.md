# Datapackage Pipelines Plus Plus

Enhance the datapackage-pipelines framework with some more opinionated architecture and easy to use code


## Features

* Object oriented processors - allows for extensibility and code re-use.
* Docker compose stack - allows for a complex architecture which is easy to setup and ensured to be the same across environments.

## Usage

### Quickstart

The common usage is to start a new code repository which will use the pipelines plus plus framework.

First, make sure you install Docker and Docker Compose - refer to Docker documentation for details.

Run the following command from within the new (or exising) project directory:

* `source <(curl -s https://raw.githubusercontent.com/OriHoch/datapackage-pipelines-plus-plus/master/bin/init-pipelines-plus-plus.sh)`

You can start the docker compose services by running:

* `bin/start.sh`

By default it provides the following services:

* Pipelines Dashboard - http://localhost:5000
* Kibana - http://localhost:15601
* Elasticsearch - http://localhost:19200
* PostgreSQL - postgresql://postgres:123456@datadb:5432/postgres
* Adminer (DB admin web ui) - http://localhost:18080

It also includes an example pipeline-spec.yaml file which generates some noise.

You can check the pipeline status in the dashboard - if it fails, it's possible elasticsearch haven't started yet.

In that case you need to wait a minute and then restart the pipelines service:

* `docker-compose restart pipelines`

Now you should see the noise pipeline running.

While it's running you can log into Adminer and Kibana to see the data as it's being committed.

A datapackage is generated under data/ directory
