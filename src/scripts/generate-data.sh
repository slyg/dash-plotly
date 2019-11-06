#!/bin/bash

echo "Generating initial data set";
if [[ -z "${endpoint}" ]] || [[ -z "${masterKey}" ]] || [[ -z "${databaseId}" ]] || [[ -z "${containerId}" ]];
    then echo "🔴 Missing some DB env variables: endpoint, masterKey, databaseId, containerId"; exit 1;
else
    python datageneration/events_28d.py;
    python datageneration/events_180d.py;
fi