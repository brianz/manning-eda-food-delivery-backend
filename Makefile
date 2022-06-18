NAME ?= brianz/food-delivery-eda

shell : ## Stars web container and opens a bash shell
	docker-compose run --rm --service-ports web bash
.PHONY: shell

build : ## Builds the containers
	docker-compose build web
.PHONY: build

dev : ## Stars web server
	docker-compose run --rm --service-ports web
.PHONY: dev

### Run these from within the Docker container

server :
	flask run --reload --host 0.0.0.0
.PHONY: server

migration :
	alembic revision --autogenerate
.PHONY: migration

migrate :
	alembic upgrade head
.PHONY: migrate

