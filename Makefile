include .env

.DEFAULT_GOAL := notebook
.image_name = slyg/dash
.container_name = dashy

build:
	docker build -t $(.image_name) .

server: build
	@docker run \
		--rm \
		-it \
		-e endpoint=$(endpoint) \
        -e masterKey=$(masterKey) \
        -e databaseId=$(databaseId) \
        -e containerId=$(containerId) \
		--name $(.container_name) \
		-v $(PWD)/src:/app \
		-p 8050:8050 \
		$(.image_name)

shell:
	@docker exec \
		-it \
		$(.container_name) \
		/bin/bash
