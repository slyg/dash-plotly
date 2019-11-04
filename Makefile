include .env

.DEFAULT_GOAL := server
.image_name = slyg/dash
.container_name = dashy
.docker_common_args = --rm \
		-it \
		-e endpoint=$(endpoint) \
        -e masterKey=$(masterKey) \
        -e databaseId=$(databaseId) \
        -e containerId=$(containerId) \
		-v $(PWD)/src:/app \
		$(.image_name)

build:
	@docker build -t $(.image_name) .

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
		--name $(.container_name) \
		$(.container_name) \
		/bin/bash

data: build
	@docker run \
		$(.docker_common_args) \
		python datageneration/events.py
