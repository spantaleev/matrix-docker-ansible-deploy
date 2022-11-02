.PHONY: lint

help: ## Show this help.
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -v grep | sed -e 's/\\$$//' | sed -e 's/##//'

lint: ## Runs ansible-lint against all roles in the playbook
	ansible-lint
