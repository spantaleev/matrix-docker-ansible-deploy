#!/bin/sh
# Fetch the synapse worker documentation and extract endpoint URLs
# matrix-org/synapse master branch points to current stable release
# and put it between `workers:start` and `workers:end` tokens in ../vars/main.yml

snippet="$(curl -L https://github.com/matrix-org/synapse/raw/master/docs/workers.md | awk -f workers-doc-to-yaml.awk)"
awk -v snippet="$snippet" -i inplace '/workers:start/{f=1;print;print snippet}/workers:end/{f=0}!f' ../vars/main.yml
