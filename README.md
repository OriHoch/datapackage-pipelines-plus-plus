# Datapackage Pipelines Plus Plus

Enhance the datapackage-pipelines framework with some more opinionated architecture and easy to use code


## Features

* Object oriented processors - allows for extensibility and code re-use.
* Docker compose stack - allows for a complex architecture which is easy to setup and ensured to be the same across environments.
* Custom processors with additional functionality.


## Installation

The common usage is to start a new code repository which will use the pipelines plus plus framework.

Run the following command from within the new (or exising) project directory:

* `source <(curl -s https://raw.githubusercontent.com/OriHoch/datapackage-pipelines-plus-plus/master/bin/init-pipelines-plus-plus.sh)`

This creates the necessary files with an example pipeline which should get you started quickly.

You should edit the README.md file and keep only the parts after the Usage header


## Usage

Following guide can be used from within any pipelines plus plus compatible project.

Only pre-requisite is to have Docker and Docker Compose installed - refer to Docker documentation for details.


### Starting the services

Start the docker compose services in the background by running:

* `bin/start.sh`

If you encounter any problems, check you docker-compose.override.yml file

* The docker-compose.override.yml file contains the docker compose stack and services configuration
* The initialization script creates it as a copy of docker-compose.override.example.yml file


### Running and debugging pipelines

Once the docker services are running you should be able to see the pipelines dashboard at:

* http://localhost:5000

The dashboard shows the status of the pipelines which are configured in the `plus_plus.source-spec.yaml` file

Usual workflow for debugging a failing pipeline:

* View pipelines logs
  * `docker-compose logs pipelines`
* Restart pipelines service - will re-run failed pipelines
  * `docker-compose restart pipelines`
* View the list of available pipelines:
  * `bin/dpp.sh`
* Run a pipeline manually
  * `bin/dpp.sh run ./pipeline/id`

The default pipeline environment provides the following services:

* Data files - should appear on the host under data/ directory
* Kibana - http://localhost:15601
  * Uses Elasticsearch on http://localhost:19200
* Adminer (DB admin web ui) - http://localhost:18080
  * Can be configured to connect to PostgreSQL - postgresql://postgres:123456@datadb:5432/postgres

Edit the docker-compose.override.yaml to enable additional services like Redash or edit the stack configuration.


## Advanced Usage


### Running locally - without Docker

The only prerequisite is to be inside an activated Python 3.6 virtualenv

From inside the virtualenv, run:

* `bin/install.sh`

This should install the required dependencies

To run the pipelines CLI you need to setup some environment variables

If the default docker stack is started, you can run:

* `source .env.example`

Otherwise, copy the file to .env, modify the environment variables

Once you set the environment variables, and ensured services are running, you can run the dpp cli directly:

* `dpp`
* `dpp run ./pipeline/id`


### Updating the pipelines plus plus framework files

If your project's code is committed to git, you can re-run `bin/init-pipelines-plus-plus.sh`

(If there is an update to the init-pipelines script itself - run it twice)

This will overwrite your files, and you can check with git what are the changes and decide how to merge them.

The only file it will not overwrite is the docker-compose.override.yml file - which you must merge manually.
