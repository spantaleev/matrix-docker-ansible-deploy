# Shows help
default:
	@just --list --justfile {{ justfile() }}

# Pulls external Ansible roles
roles:
	rm -rf roles/galaxy
	ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force

# Runs ansible-lint against all roles in the playbook
lint:
	ansible-lint

# Runs the playbook with --tags=install-all,ensure-matrix-users-created,start and optional arguments
install-all *extra_args: (run-tags "install-all,ensure-matrix-users-created,start" extra_args)

# Runs the playbook with --tags=setup-all,ensure-matrix-users-created,start and optional arguments
setup-all *extra_args: (run-tags "setup-all,ensure-matrix-users-created,start" extra_args)

# Runs the playbook with the given list of arguments
run +extra_args:
	time ansible-playbook -i inventory/hosts setup.yml {{ extra_args }}

# Runs the playbook with the given list of comma-separated tags and optional arguments
run-tags tags *extra_args:
	just --justfile {{ justfile() }} run --tags={{ tags }} {{ extra_args }}

# Runs the playbook in user-registration mode
register-user username password admin_yes_or_no *extra_args:
	time ansible-playbook -i inventory/hosts setup.yml --tags=register-user --extra-vars="username={{ username }} password={{ password }} admin={{ admin_yes_or_no }}" {{ extra_args }}

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
