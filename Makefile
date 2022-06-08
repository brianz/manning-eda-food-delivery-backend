NAME ?= brianz/food-delivery-eda

build : ## Builds the containers
	docker-compose build web
.PHONY: build

dev : ## Stars web server
	docker-compose run --rm --service-ports web
.PHONY: dev

shell : ## Stars web container and opens a bash shell
	docker-compose run --rm --service-ports web bash
.PHONY: shell