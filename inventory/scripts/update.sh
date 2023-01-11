#!/usr/bin/env bash
#
# Wrapper script for the entire update procedure including
#   * updating git repo
#   * downloading roles
#   * running playbook
#
# This script first asks for the passwords for all the hosts and then pipes them
# to the ansible playbook wrapper script, so that we don't need to wait for the
# merging and downloading to finish, before being asked for the passwords.
#

# exit on errors
set -e

# set playbook root path
root=$(dirname "$(readlink -f "$0")")/../..

# capture passwords for all hosts
for host in "$root"/inventory/*.yml; do
    read -rp "sudo password for $(basename "$host"): " -s pw
    pipeinput+="$pw\n"
    echo
done

# merge upstream master branch
git -C "$root" pull upstream master

# check the changelog before updating
less CHANGELOG.md
read -r

# download upstream roles
make -f "$root"/Makefile roles

# run ansible-playbook on all hosts
echo -e "$pipeinput" | bash "$root"/inventory/scripts/ansible-all-hosts.sh
