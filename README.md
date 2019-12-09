# RSE dashboard [![Build Status](https://dev.azure.com/hmcts/Software%20Engineering/_apis/build/status/hmcts.RSE-dashboard?branchName=master)](https://dev.azure.com/hmcts/Software%20Engineering/_build/latest?definitionId=273&branchName=master)

This application displays a variety of data about CI and security

![Screenshot](https://user-images.githubusercontent.com/602143/68217085-e9fa6c80-ffd9-11e9-9218-5e63fb14f17f.png)

## Available commands

```
$ make help

Available commands:

	make build                 Creates the development container image
	make data                  (Re)generates all data sets
	make help                  Displays this help section (default target)
	make production-image      Creates docker image to be deployed
	make server                Starts the development server (default)
	make session               Starts a new interactive development container
	make shell                 Opens a shell session on the development container

```

## CI

Here are the expected environment variables to expose in the CI:

| Name                        | Comment                                              |
| --------------------------- | ---------------------------------------------------- |
| `azureContainerRegistry`    | E.g.: my-registry.azurecr.io                         |
| `azureSubscriptionEndpoint` | Service connection to azure container registry (ACR) |
| `masterKey`                 | CosmosDB masterKey                                   |
| `containerId`               | CosmosDB container ID                                |
| `databaseId`                | CosmosDB database ID                                 |
| `endpoint`                  | Endpoint of the DB                                   |
| `githubtoken`               | Github Access token used to query the Github API     |
