#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Checks that the Jinja expressions in the playbook's group_vars files can be parsed.
#
# Ansible renders a `{{ ... }}` expression in group_vars only when something uses that value,
# usually a role's task. A typo such as a missing `)` or `'` can therefore pass `--syntax-check`
# and the ansible-lint hook (which only lints roles/custom), and the playbook run fails where the
# value is first used.
# This script reads the file as YAML, parses every string value with Jinja2 (as Ansible does before
# evaluating it), and prints the variable name and line of each value that does not parse.
# It checks syntax only: it does not know which variables or filters exist.
#
# Usage: bin/check-group-vars-jinja.py group_vars/matrix_servers group_vars/jitsi_jvb_servers

import sys

import jinja2
import yaml


def string_values(node, variable):
    """Yields (variable, node) for every string value below a YAML node."""
    if node.tag == "!unsafe":  # Ansible never evaluates values tagged !unsafe
        return
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            yield from string_values(value, variable or key.value)
    elif isinstance(node, yaml.SequenceNode):
        for value in node.value:
            yield from string_values(value, variable)
    else:
        yield variable, node


def main(paths):
    environment = jinja2.Environment()
    failed = False
    for path in paths:
        try:
            with open(path, encoding="utf-8") as file:
                document = yaml.compose(file, Loader=yaml.SafeLoader)
        except yaml.YAMLError as error:
            print(f"{path}: invalid YAML: {error}")
            failed = True
            continue
        if document is None:
            print(f"{path}:1: empty YAML document")
            failed = True
            continue
        for variable, node in string_values(document, None):
            try:
                environment.parse(node.value)
            except jinja2.TemplateSyntaxError as error:
                line = node.start_mark.line + 1
                print(f"{path}:{line}: {variable}: {error.message} (line {error.lineno} of the value)")
                failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
