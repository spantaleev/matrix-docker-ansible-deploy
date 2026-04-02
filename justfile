# SPDX-FileCopyrightText: 2023 - 2024 Nikita Chernyi
# SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
# SPDX-FileCopyrightText: 2024 Suguru Hirahara
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# mise (dev tool version manager)
mise_data_dir := env("MISE_DATA_DIR", justfile_directory() / "var/mise")
mise_trusted_config_paths := justfile_directory() / "mise.toml"
prek_home := env("PREK_HOME", justfile_directory() / "var/prek")

# Shows help
default:
    @{{ just_executable() }} --list --justfile "{{ justfile() }}"

# Initialize inventory files
inventory domain ip:
    #!/usr/bin/env sh
    VARS_DIR="inventory/host_vars/{{ domain }}"
    VARS_FILE="inventory/host_vars/{{ domain }}/vars.yml"
    HOSTS_FILE="inventory/hosts"

    mkdir -p "$VARS_DIR"
    cp examples/vars.yml "$VARS_FILE"
    cp examples/hosts inventory/hosts
    sed -i 's/^matrix_domain:.*/matrix_domain: {{ domain }}/' "$VARS_FILE"
    PASSWORD=`openssl rand -base64 64 | head -c 64`; \
        sed -i "s#^matrix_homeserver_generic_secret_key:.*#matrix_homeserver_generic_secret_key: '$PASSWORD'#" "$VARS_FILE"
    sed -i 's/^matrix\.example\.com/{{ domain }}/'          "$HOSTS_FILE"
    sed -i 's/ansible_host=<[^>]\+>/ansible_host={{ ip }}/' "$HOSTS_FILE"
    echo "Check and configure your files at:"
    echo $VARS_FILE
    echo $HOSTS_FILE


# Pulls external Ansible roles
roles:
    #!/usr/bin/env sh
    echo "[NOTE] This command just updates the roles, but if you want to update everything at once (playbook, roles, etc.) - use 'just update'"
    if [ -x "$(command -v agru)" ]; then
    	agru
    else
    	rm -rf roles/galaxy
    	ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
    fi

# Updates the playbook and installs the necessary Ansible roles pinned in requirements.yml. If a -u flag is passed, also updates the requirements.yml file with new role versions (if available)
update *flags: update-playbook-only
    #!/usr/bin/env sh
    if [ -x "$(command -v agru)" ]; then
        echo {{ if flags == "" { "Installing roles pinned in requirements.yml…" } else { if flags == "-u" { "Updating roles and pinning new versions in requirements.yml…" } else { "Unknown flags passed" } } }}
        agru {{ flags }}
    else
        echo "[NOTE] You are using the standard ansible-galaxy tool to install roles, which is slow and lacks other features. We recommend installing the 'agru' tool to speed up the process: https://github.com/etkecc/agru#where-to-get"
        echo "Installing roles…"
        rm -rf roles/galaxy
        ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
    fi

# Updates the playbook without installing/updating Ansible roles
update-playbook-only:
    @echo "Updating playbook…"
    @git stash -q
    @git pull -q
    @-git stash pop -q

# Invokes mise with the project-local data directory
mise *args: _ensure_mise_data_directory
    #!/bin/sh
    export MISE_DATA_DIR="{{ mise_data_dir }}"
    export MISE_TRUSTED_CONFIG_PATHS="{{ mise_trusted_config_paths }}"
    export MISE_YES=1
    export PREK_HOME="{{ prek_home }}"
    mise {{ args }}

# Runs prek (pre-commit hooks manager) with the given arguments
prek *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile "{{ justfile() }}" mise exec -- prek {{ args }}

# Runs pre-commit hooks on staged files
prek-run-on-staged *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile "{{ justfile() }}" prek run {{ args }}

# Runs pre-commit hooks on all files
prek-run-on-all *args: _ensure_mise_tools_installed
    @{{ just_executable() }} --justfile "{{ justfile() }}" prek run --all-files {{ args }}

# Installs the git pre-commit hook
prek-install-git-pre-commit-hook: _ensure_mise_tools_installed
    #!/usr/bin/env sh
    set -eu
    {{ just_executable() }} --justfile "{{ justfile() }}" mise exec -- prek install
    hook="{{ justfile_directory() }}/.git/hooks/pre-commit"
    # The installed git hook runs later under Git, outside this just/mise environment.
    # Injecting PREK_HOME keeps prek's cache under var/prek instead of a global home dir,
    # which is more predictable and works better in sandboxed tools like Codex/OpenCode.
    if [ -f "$hook" ] && ! grep -q '^export PREK_HOME=' "$hook"; then
        sed -i '2iexport PREK_HOME="{{ prek_home }}"' "$hook"
    fi

# Runs the playbook with --tags=install-all,ensure-matrix-users-created,start and optional arguments
install-all *extra_args: (run-tags "install-all,ensure-matrix-users-created,start" extra_args)

# Runs installation tasks for a single service
install-service service *extra_args:
    {{ just_executable() }} --justfile "{{ justfile() }}" run \
    --tags=install-{{ service }},start-group \
    --extra-vars=group={{ service }} {{ extra_args }}

# Runs the playbook with --tags=setup-all,ensure-matrix-users-created,start and optional arguments
setup-all *extra_args: (run-tags "setup-all,ensure-matrix-users-created,start" extra_args)

# Runs the playbook with the given list of arguments
run +extra_args:
    ansible-playbook -i inventory/hosts setup.yml {{ extra_args }}

# Runs the playbook with the given list of comma-separated tags and optional arguments
run-tags tags *extra_args:
    {{ just_executable() }} --justfile "{{ justfile() }}" run --tags={{ tags }} {{ extra_args }}

# Runs the playbook in user-registration mode
register-user username password admin_yes_or_no *extra_args:
    ansible-playbook -i inventory/hosts setup.yml --tags=register-user --extra-vars="username={{ username }} password={{ password }} admin={{ admin_yes_or_no }}" {{ extra_args }}

# Starts all services
start-all *extra_args: (run-tags "start-all" extra_args)

# Starts a specific service group
start-group group *extra_args:
    @{{ just_executable() }} --justfile "{{ justfile() }}" run-tags start-group --extra-vars="group={{ group }}" {{ extra_args }}

# Stops all services
stop-all *extra_args: (run-tags "stop-all" extra_args)

# Stops a specific service group
stop-group group *extra_args:
    @{{ just_executable() }} --justfile "{{ justfile() }}" run-tags stop-group --extra-vars="group={{ group }}" {{ extra_args }}

# Rebuilds the mautrix-meta-instagram Ansible role using the mautrix-meta-messenger role as a source
rebuild-mautrix-meta-instagram:
    /bin/bash "{{ justfile_directory() }}/bin/rebuild-mautrix-meta-instagram.sh" "{{ justfile_directory() }}/roles/custom"

# Internal - ensures var/mise and var/prek directories exist
_ensure_mise_data_directory:
    @mkdir -p "{{ mise_data_dir }}"
    @mkdir -p "{{ prek_home }}"

# Internal - ensures mise tools are installed
_ensure_mise_tools_installed: _ensure_mise_data_directory
    @{{ just_executable() }} --justfile "{{ justfile() }}" mise install --quiet
