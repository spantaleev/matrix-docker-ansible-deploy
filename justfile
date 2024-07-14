# Shows help
default:
    @just --list --justfile {{ justfile() }}

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

# Updates requirements.yml if there are any new tags available. Supported flags: -u (update roles, if any new tags are available)
update *flags: update-self
    #!/usr/bin/env sh
    if [ -x "$(command -v agru)" ]; then
        echo {{ if flags == "" { "installing roles..." } else if flags == "-u" { "updating roles..." } else { "unknown flag passed" } }}
        agru {{ flags }}
    else
        echo "[NOTE] you are using standard ansible-galaxy to install roles, it's slow and cannot update roles if there are newer tags available. We recommend to install 'agru' tool to speed up the process: https://gitlab.com/etke.cc/tools/agru#where-to-get"
        echo "installing roles..."
        rm -rf roles/galaxy
        ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force
    fi

# update playbook
update-self:
    @echo "updating playbook..."
    @git stash -q
    @git pull -q
    @-git stash pop -q

# Runs ansible-lint against all roles in the playbook
lint:
    ansible-lint

# Runs the playbook with --tags=install-all,ensure-matrix-users-created,start and optional arguments
install-all *extra_args: (run-tags "install-all,ensure-matrix-users-created,start" extra_args)

# Runs installation tasks for a single service
install-service service *extra_args:
    just --justfile {{ justfile() }} run \
    --tags=install-{{ service }},start-group \
    --extra-vars=group={{ service }} \
    --extra-vars=devture_systemd_service_manager_service_restart_mode=one-by-one {{ extra_args }}

# Runs the playbook with --tags=setup-all,ensure-matrix-users-created,start and optional arguments
setup-all *extra_args: (run-tags "setup-all,ensure-matrix-users-created,start" extra_args)

# Runs the playbook with the given list of arguments
run +extra_args:
    ansible-playbook -i inventory/hosts setup.yml {{ extra_args }}

# Runs the playbook with the given list of comma-separated tags and optional arguments
run-tags tags *extra_args:
    just --justfile {{ justfile() }} run --tags={{ tags }} {{ extra_args }}

# Runs the playbook in user-registration mode
register-user username password admin_yes_or_no *extra_args:
    ansible-playbook -i inventory/hosts setup.yml --tags=register-user --extra-vars="username={{ username }} password={{ password }} admin={{ admin_yes_or_no }}" {{ extra_args }}

# Starts all services
start-all *extra_args: (run-tags "start-all" extra_args)

# Starts a specific service group
start-group group *extra_args:
    @just --justfile {{ justfile() }} run-tags start-group --extra-vars="group={{ group }}" {{ extra_args }}

# Stops all services
stop-all *extra_args: (run-tags "stop-all" extra_args)

# Stops a specific service group
stop-group group *extra_args:
    @just --justfile {{ justfile() }} run-tags stop-group --extra-vars="group={{ group }}" {{ extra_args }}

# Rebuilds the mautrix-meta-instagram Ansible role using the mautrix-meta-messenger role as a source
rebuild-mautrix-meta-instagram:
    /bin/bash {{ justfile_directory() }}/bin/rebuild-mautrix-meta-instagram.sh {{ justfile_directory() }}/roles/custom
