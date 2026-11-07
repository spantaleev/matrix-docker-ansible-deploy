#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Checks that each `install-SERVICE` tag of the custom roles has a matching service group.
#
# `just install-service SERVICE` runs the `install-SERVICE` tag and then starts the group named SERVICE.
# Ansible does not complain if that group does not exist, so the service gets installed, but not started.
#
# This script does not cover:
# - tags of the galaxy roles, because they are not available where this hook runs in CI
# - whether a group contains all of a role's services, as the group only needs to exist here
# - group names which have no matching tag, as these are valid for `just start-group` and `just stop-group`
#
# Usage: bin/check-install-service-names.py

import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
GROUP_VARS = REPO / "group_vars" / "matrix_servers"
ROLES = REPO / "roles" / "custom"
SERVICES_VARIABLE = "devture_systemd_service_manager_services_list_auto"

# The homeserver's service uses `matrix_homeserver_implementation` as a group name.
# The values below are the ones allowed by the matrix-base role's validate_config.yml.
HOMESERVER_IMPLEMENTATIONS = {"synapse", "dendrite", "conduit", "continuwuity", "tuwunel"}

# Tags of custom roles which do not install a service of their own, so no group can match them.
TAGS_WITHOUT_SERVICE = {
    "appservice-double-puppet",  # only prepares configuration for other services
    "docker",  # only used for migration tasks here, as the Docker role itself is a galaxy one
    "prometheus-services-connect",  # only prepares configuration for other services
}


def tag_names(node):
    """Yields the tag names below a YAML node, whichever way a task has them written."""
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            if key.value == "tags":
                if isinstance(value, yaml.SequenceNode):
                    yield from (item.value for item in value.value)
                else:
                    yield from (tag.strip() for tag in value.value.split(","))
            else:
                yield from tag_names(value)
    elif isinstance(node, yaml.SequenceNode):
        for value in node.value:
            yield from tag_names(value)


def install_tags():
    """Returns a map of service names (tags without the `install-` prefix) to the roles having them."""
    services = {}
    for path in sorted(ROLES.glob("*/tasks/**/*.yml")):
        role = path.relative_to(ROLES).parts[0]
        with path.open(encoding="utf-8") as file:
            for tag in tag_names(yaml.compose(file, Loader=yaml.SafeLoader)):
                if tag.startswith("install-") and tag != "install-all":
                    services.setdefault(tag.removeprefix("install-"), set()).add(role)
    return services


def service_groups():
    """Returns the group names used in the list of services."""
    with GROUP_VARS.open(encoding="utf-8") as file:
        document = yaml.compose(file, Loader=yaml.SafeLoader)
    value = next(value.value for key, value in document.value if key.value == SERVICES_VARIABLE)
    groups = set()
    for names in re.findall(r"'groups': \[(.*?)\]", value):
        groups.update(re.findall(r"'([^']+)'", names))
    if "'groups': ['matrix', 'homeservers', matrix_homeserver_implementation]" in value:
        groups.update(HOMESERVER_IMPLEMENTATIONS)
    return groups


def main():
    services = install_tags()
    groups = service_groups()
    failed = False
    for service, roles in sorted(services.items()):
        if service not in groups and service not in TAGS_WITHOUT_SERVICE:
            print(f"install-{service} ({', '.join(sorted(roles))}): no `{service}` group in {SERVICES_VARIABLE}")
            failed = True
    for service in sorted(TAGS_WITHOUT_SERVICE):
        if service not in services:
            print(f"{service}: listed in TAGS_WITHOUT_SERVICE, but no custom role has an install-{service} tag")
            failed = True
        elif service in groups:
            print(f"{service}: listed in TAGS_WITHOUT_SERVICE, but it has a group")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
