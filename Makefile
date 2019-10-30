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
		--name $(.container_name) \
		-v $(PWD)/src:/app \
		-p 8050:8050 \
		$(.image_name)

build:
	docker build -t $(.image_name) .

server: build
	@docker run $(.docker_common_args)

session: build
	@docker run $(.docker_common_args) /bin/bash

shell:
	@docker exec \
		-it \
		$(.container_name) \
		/bin/bash
