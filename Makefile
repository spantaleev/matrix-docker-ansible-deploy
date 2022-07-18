.PHONY: lint

help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

lint: ## Runs ansible-lint against all roles in the playbook
	ansible-lint
