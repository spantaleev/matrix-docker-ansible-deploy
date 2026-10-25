#!/bin/sh
# SPDX-FileCopyrightText: 2026 MASH project contributors
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Runs Python (with the given arguments) using the interpreter which runs Ansible.
#
# The playbook's Python scripts need PyYAML, which Ansible depends on. The interpreter which runs Ansible
# therefore has it, even when Ansible is installed in an environment of its own (e.g. with pipx),
# where the system's `python3` may lack it.
#
# The interpreter is taken from the first line (shebang) of `ansible-playbook`.
# If that is not a Python interpreter (e.g. `ansible-playbook` is a wrapper script, or Gentoo's python-exec),
# Ansible is asked which interpreter it runs on. If that fails too, or Ansible is not installed, `python3` is used.

set -eu

interpreter=

ansible_playbook_path=$(command -v ansible-playbook 2>/dev/null || true)
if [ -n "$ansible_playbook_path" ] && [ -f "$ansible_playbook_path" ]; then
    shebang=$(head -n 1 "$ansible_playbook_path")
    case "$shebang" in
        "#!"*)
            read -r interpreter next_word _ <<EOF
${shebang#"#!"}
EOF
            # `#!/usr/bin/env python3` names the interpreter in the next word
            if [ "$(basename "$interpreter")" = "env" ]; then
                interpreter=${next_word:-}
            fi
            ;;
    esac

    # Only names like `python`, `python3` or `python3.14` are interpreters (`python-exec2c` is not)
    case "$(basename "${interpreter:-none}")" in
        python | python[0-9] | python[0-9].[0-9]*) ;;
        *) interpreter= ;;
    esac

    if [ -z "$interpreter" ] || ! command -v "$interpreter" >/dev/null 2>&1; then
        # The interpreter ends a line like: `  python version = 3.14.0 (main, …) [GCC …] (/usr/bin/python3.14)`
        interpreter=$("$ansible_playbook_path" --version 2>/dev/null \
            | sed -n 's/^ *python version = .*(\([^()]*\))$/\1/p' | head -n 1) || true
    fi
fi

if [ -n "$interpreter" ] && command -v "$interpreter" >/dev/null 2>&1; then
    python=$interpreter
else
    python=python3
fi

exec "$python" "$@"
