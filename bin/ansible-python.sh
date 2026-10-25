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
# If that is not a Python interpreter (e.g. `ansible-playbook` is a wrapper script), or Ansible is not installed,
# `python3` is used.

set -eu

python=python3

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
            case "$(basename "${interpreter:-none}")" in
                python*)
                    if command -v "$interpreter" >/dev/null 2>&1; then
                        python=$interpreter
                    fi
                    ;;
            esac
            ;;
    esac
fi

exec "$python" "$@"
