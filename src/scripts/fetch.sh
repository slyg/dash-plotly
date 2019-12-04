#!/bin/bash

set -e;
echo "Fetching data (can take a few minutes)";
python datageneration/cve_suppressions.py & \
python datageneration/events_28d.py & \
python datageneration/events_180d.py & \
python datageneration/js_apps.py & \
python datageneration/node_versions.py & \
python datageneration/java_versions.py & \
wait;