#!/bin/bash

set -e;
echo "Fetching data (can take a few minutes)";
python datageneration/events_28d.py & \
python datageneration/events_180d.py & \
wait;