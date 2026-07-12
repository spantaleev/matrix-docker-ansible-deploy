# SPDX-FileCopyrightText: 2022 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

.PHONY: roles lint add-inventory-host

help: ## Show this help.
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\\$$//' | sed -e 's/##//'

add-inventory-host: ## Adds a new host to the inventory, creating the inventory files if necessary (e.g. `make add-inventory-host domain=example.com ip=1.2.3.4`)
	@./bin/add-inventory-host.sh "$(domain)" "$(ip)"

roles: ## Pull roles
	rm -rf roles/galaxy
	ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force

lint: ## Runs ansible-lint against all roles in the playbook
	ansible-lint roles/custom
