#!/bin/bash

set -e;

if [[ -z "${endpoint}" ]] || [[ -z "${masterKey}" ]] || [[ -z "${databaseId}" ]] || [[ -z "${containerId}" ]];
    then echo "🔴 Missing some DB env variables: endpoint, masterKey, databaseId, containerId"; exit 1;
else
    echo "Generating initial data set";

    python datageneration/events_28d.py;
    python datageneration/events_180d.py;

    echo "Starting app";

    python app.py;
fi