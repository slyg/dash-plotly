.container_name = dashy

build:
	docker build -t slyg/dash .

server: build
	@docker run \
		--rm \
		-it \
		--name $(.container_name) \
		-v $(PWD)/src:/app \
		-p 8050:8050 \
		slyg/dash

shell:
	@docker exec \
		-it \
		$(.container_name) \
		/bin/bash
