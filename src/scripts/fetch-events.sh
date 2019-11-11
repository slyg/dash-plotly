#!/bin/bash

set -e;
echo "Fetching data";
python datageneration/events_28d.py;
python datageneration/events_180d.py;