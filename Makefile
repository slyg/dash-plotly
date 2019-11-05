include .env

.DEFAULT_GOAL := server
.image_name = slyg/dash-local
.image_name_production = hmcts/rse-dashboard
.container_name = dashy
.docker_common_args = --rm \
		-it \
		-e endpoint=$(endpoint) \
        -e masterKey=$(masterKey) \
        -e databaseId=$(databaseId) \
        -e containerId=$(containerId) \
		-v $(PWD)/src:/app \
		$(.image_name)
.dev_docker_image = ./local.Dockerfile

build:
	@docker build \
		-f $(.dev_docker_image) \
		-t $(.image_name) \
		.

server: build
	@docker run \
		--name $(.container_name) \
		-p 8050:8050 \
		$(.docker_common_args)

session: build
	@docker run \
		--name $(.container_name) \
		-p 8050:8050 \
		$(.docker_common_args) \
		/bin/bash

shell:
	@docker exec \
		-it \
		$(.container_name) \
		/bin/bash

data-short: build
	@docker run \
		$(.docker_common_args) \
		python datageneration/events_28d.py

data-long: build
	@docker run \
		$(.docker_common_args) \
		python datageneration/events_180d.py

production-image:
	@docker build \
	-t $(.image_name_production) \
	.