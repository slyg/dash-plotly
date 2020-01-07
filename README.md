# RSE dashboard [![Build Status](https://dev.azure.com/hmcts/Software%20Engineering/_apis/build/status/hmcts.RSE-dashboard?branchName=master)](https://dev.azure.com/hmcts/Software%20Engineering/_build/latest?definitionId=273&branchName=master)

This application displays a variety of data about CI and security

![Screenshot](https://user-images.githubusercontent.com/602143/68217085-e9fa6c80-ffd9-11e9-9218-5e63fb14f17f.png)

## Prerequisites

- Docker
- GNU Make
- an `.env` file as per the sample `.env.sample`

See also the [CD](#cd) section for details about the `.env` file.

## Available commands

```
$ make help

Available commands:

	make build                 Creates the development container image
	make data                  (Re)generates all data sets
	make help                  Displays this help section (default target)
	make production-image      Creates docker image to be deployed
	make server                Starts the development server
	make session               Starts a new interactive development container
	make shell                 Opens a shell session on the development container
	make tests                 Runs unit tests

```

## Local setup

To locally run and see the effects of a code change, you can use the following steps:

|     | Step                           | Command                   | Comment                                                |
| --- | ------------------------------ | ------------------------- | ------------------------------------------------------ |
| 1.  | Start a shell in the container | `$ make session`          | The filetree under `src/` is shared with the container |
| 2.  | Fetch data                     | `# sh ./scripts/fetch.sh` | Needed only once                                       |
| 3.  | Start the application          | `# python server.py`      | You may restart the application to see your changes    |

The local app is exposed at `http://localhost:8050`

## Application structure

The dashboard pages are added via a middleware to a root Flask application (`src/server.py`). They are themselves fully-fledged Flask applications using the plotly/dash utility library. It is a bit convoluted, however dash applications do not allow multiple pages at the moment, unfortunately.

The figures are exposed as memoized functions via a decorator, hence a first rendering taking quite some time to format the raw data in a shape that can be graphed. Further calls are much quicker.

```bash
src
├── dash_apps 			# Dash applications (Main exposed pages)
│   ├── assets 			# Static assets that cannot be picked up from the parent /style folder
│   ├── components		# Common UI component used in Dash applications (layout, etvc.)
│   ├── figures 		# Figures displayed in the Dash apps (exposed as functions)
│   ├── lib 			# Shared data transformation libraries
│   ├── server_pipelines.py 	# Pipeline Dash app/page
│   └── server_security.py 	# Security Dash app/page
├── data 			# Folder containing pulled data
├── datageneration 		# Scripts used to pull data
├── scripts 			# Shortcuts for data generation scripts
├── server.py 			# Root web server app (Flask)
├── static 			# Static assets (images, css, etc.)
├── style 			# Styles used by the dash applications (gradients, colors, etc.)
└── templates 			# Auxiliary pages templates (disclaimer, etc.)

```

## CD

Here are the expected environment variables to expose to the azure devops pipeline (link on the badge):

| Name                        | Comment                                              |
| --------------------------- | ---------------------------------------------------- |
| `azureContainerRegistry`    | E.g.: my-registry.azurecr.io                         |
| `azureSubscriptionEndpoint` | Service connection to azure container registry (ACR) |
| `masterKey`                 | CosmosDB masterKey                                   |
| `containerId`               | CosmosDB container ID                                |
| `databaseId`                | CosmosDB database ID                                 |
| `endpoint`                  | Endpoint of the DB                                   |
| `githubtoken`               | Github Access token used to query the Github API     |

### Build strategy

This project is bundled as a single docker image containing a web application.
The exposed data is created at build time, using the above secrets. These secrets are dropped in the final image using multi-stage build.

Only master branch changes trigger a new build.

The CI is also scheduled to rebuild a new image from the master branch every 2 hours on work hours on weekdays, as specified in the `azure-pipeline.yml` file. Notice the number of build per schedule is capped at 100/w for azure devops pipelines.

The build image is pushed to an ACR and deployed via an app service.

Updating data is done by triggering a new build, and therefore triggering a new deployment.

Here are the details you may need to track these processes:

| Name         | Value                                                                                 |
| ------------ | ------------------------------------------------------------------------------------- |
| ACR          | `$azureContainerRegistry` specified in the CI                                         |
| Image name   | `hmcts/rse-dashboard`                                                                 |
| App Service  | `rse-dashboard`                                                                       |
| Exposed port | Passed via the `--env PORT` argument (the App Service picks a random port by default) |
| VNet         | `rse-dashboard-vnet`                                                                  |

### Project deletion

In the case you want to cleanly remove this project and its related CI and runtime, here is a checklist of the resources you may remove:

- VNet `rse-dashboard-vnet`
- App Service `rse-dashboard`
- ACR registry `hmcts/rse-dashboard` (sandbox)
- Azure devops pipeline ([link](https://dev.azure.com/hmcts/Software%20Engineering/_build/latest?definitionId=273&branchName=master))
- Remove the github token used in the CI (depending on who is the owner of it)
- Archive or delete this repo
