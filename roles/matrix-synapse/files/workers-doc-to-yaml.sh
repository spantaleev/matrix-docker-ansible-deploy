#!/bin/sh
# Fetch the synapse worker documentation and extract endpoint URLs
# matrix-org/synapse master branch points to current stable release

URL=https://github.com/matrix-org/synapse/raw/master/docs/workers.md
curl -L ${URL} | awk -f workers-doc-to-yaml.awk > ../vars/workers.yml
