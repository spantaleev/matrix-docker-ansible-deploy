# SPDX-FileCopyrightText: 2022 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

.PHONY: roles lint

VARS_DIR   := inventory/host_vars/$(domain)
VARS_FILE  := inventory/host_vars/$(domain)/vars.yml
HOSTS_FILE := inventory/hosts

help: ## Show this help.
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\\$$//' | sed -e 's/##//'

inventory: ## Initialize inventory files
	@mkdir -p "$(VARS_DIR)"
	@cp examples/vars.yml "$(VARS_FILE)"
	@cp examples/hosts inventory/hosts
	@sed -i 's/^matrix_domain:.*/matrix_domain: $(domain)/' "$(VARS_FILE)"
	@PASSWORD=`openssl rand -base64 64 | head -c 64`; \
		sed -i "s#^matrix_homeserver_generic_secret_key:.*#matrix_homeserver_generic_secret_key: '$$PASSWORD'#" "$(VARS_FILE)"
	@sed -i 's/^matrix\.example\.com/$(domain)/'          "$(HOSTS_FILE)"
	@sed -i 's/ansible_host=<[^>]\+>/ansible_host=$(ip)/' "$(HOSTS_FILE)"
	@echo "Check and configure your files at:"
	@echo $(VARS_FILE)
	@echo $(HOSTS_FILE)

roles: ## Pull roles
	rm -rf roles/galaxy
	ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force

lint: ## Runs ansible-lint against all roles in the playbook
	ansible-lint roles/custom
