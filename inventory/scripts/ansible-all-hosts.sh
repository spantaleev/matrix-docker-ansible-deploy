#!/usr/bin/env bash
#
# Run the playbook on multiple hosts with different credentials with this script
# It defaults to ansible tags "setup-all,start". You can pass alternative tags
# to this script as arguments, e.g.
#
#     ./inventory/scripts/ansible-all-hosts.sh self-check
#

# set inventory directory path
inventory=$(dirname "$(readlink -f "$0")")/../../inventory

# set default tags or get from first argument if any
tags="${1:-setup-all,start}"

# init password array
declare -A pws

# capture passwords for all hosts
for host in "$inventory"/*.yml; do
    read -rp "sudo password for $(basename "$host"): " -s pw
    pws[$host]="$pw"
    echo
done

# run ansible on all captured passwords/hosts
for host in "${!pws[@]}"; do
    ansible-playbook setup.yml \
        --inventory-file "$host" \
        --extra-vars "ansible_become_pass=${pws[$host]}" \
        --tags="$tags"
done
