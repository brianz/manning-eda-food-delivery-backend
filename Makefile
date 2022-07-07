NAME ?= brianz/food-delivery-eda

shell : ## Stars web container and opens a bash shell
	docker-compose run --rm --service-ports web bash
.PHONY: shell

bash : ## Open up a new bash shell to an already running container
	docker exec -it \
		`docker ps -f name=manning-eda-food-delivery-backend_web --format "{{.ID}}"` bash
.PHONY: bash

build : ## Builds the containers
	docker-compose build web
.PHONY: build

dev : ## Stars web server
	docker-compose run --rm --service-ports web
.PHONY: dev

stop : ## Stop all of the running containers
	docker-compose stop
.PHONY: stop

rmdb : ## Delete the database container and start over
	docker-compose rm -f psql
.PHONY: rmdb

####################################################
### Run these from within the Docker container
####################################################

server : ## Run the flask server with hot reload enabled
	flask run --reload --host 0.0.0.0
.PHONY: server

migration : ## Create a new migration file whenver there are changes to the DB / ORM
	alembic revision --autogenerate
.PHONY: migration

migrate : ## Apply all of the DB migrations, creating new tables and updating other things.
	alembic upgrade head
.PHONY: migrate

data :
	FLASK_APP=/code/src/admin.py flask create-data
.PHONY: data

pipenv : ## Install the pipenv environments, taking the dev environment into account
ifeq ($(ENV),dev)
	pipenv install --system --dev
else
	pipenv install --system
endif
.PHONY: pipenv
