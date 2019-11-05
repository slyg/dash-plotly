# RSE dashboard

This application displays a variety of data about CI and security

![Screenshot](https://user-images.githubusercontent.com/602143/68217085-e9fa6c80-ffd9-11e9-9218-5e63fb14f17f.png)

## Available commands

```
$ make help

Available commands:

	make build                 Creates the development container image
	make data                  (Re)generates all data sets
	make data-long             (Re)generates long-term data sets (takes time)
	make data-short            (Re)generates short-term data sets
	make help                  Displays this help section (default target)
	make production-image      Creates docker image to be deployed
	make server                Starts the development server (default)
	make session               Starts a new interactive development container
	make shell                 Opens a shell session on the development container

```