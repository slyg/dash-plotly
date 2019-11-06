SHELL := /bin/bash
.DEFAULT_GOAL := server
.image_name = slyg/dash-local
.image_name_production = hmcts/rse-dashboard
.container_name = dashy
.docker_common_args = --rm \
		-it \
		-e endpoint=$$endpoint \
        -e masterKey=$$masterKey \
        -e databaseId=$$databaseId \
        -e containerId=$$containerId \
		-v $(PWD)/src:/app \
		$(.image_name)
.dev_docker_image = ./local.Dockerfile

.PHONY: build ## Creates the development container image
build:
	@docker build \
		-f $(.dev_docker_image) \
		-t $(.image_name) \
		.

.PHONY: server ## Starts the development server (default)
server: build
	@. .env; docker run \
		--name $(.container_name) \
		-p 8050:8050 \
		$(.docker_common_args)

.PHONY: session ## Starts a new interactive development container
session: build
	@. .env; docker run \
		--name $(.container_name) \
		-p 8050:8050 \
		$(.docker_common_args) \
		/bin/bash

.PHONY: shell ## Opens a shell session on the development container
shell:
	@docker exec \
		-it \
		$(.container_name) \
		/bin/bash

.PHONY: data-short ## (Re)generates short-term data sets
data-short: build
	@. .env
	@docker run \
		$(.docker_common_args) \
		python datageneration/events_28d.py

.PHONY: data-long ## (Re)generates long-term data sets (takes time)
data-long: build
	@. .env; docker run \
		$(.docker_common_args) \
		python datageneration/events_180d.py

.PHONY: data ## (Re)generates all data sets
data: data-short data-long

.PHONY: production-image ## Creates docker image to be deployed
production-image:
	@. .env; docker build \
		--build-arg endpoint=$$endpoint \
        --build-arg masterKey=$$masterKey \
        --build-arg databaseId=$$databaseId \
        --build-arg containerId=$$containerId \
		-t $(.image_name_production) \
		.

.PHONY: deploy ## Deployment script used by CI
deploy:
	@echo Not implemented

.PHONY: help ## Displays this help section (default target)
help:
	@echo ""
	@echo "  Available commands:"
	@echo ""
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m\tmake %-20s\033[0m %s\n", $$2, $$3}'
	@echo ""