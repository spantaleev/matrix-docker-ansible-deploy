#!/bin/bash
# Runs a role's Molecule scenario locally.
#
# Called through `just molecule [role] [args...]`. With no role, lists the roles
# that have a scenario.
#
# The same scenarios run in CI (.github/workflows/molecule.yml), but running one
# here is the faster loop while writing or fixing a role: CI only tells you after
# a push, and only about the roles that push touched.
#
# Deliberately NOT wired into prek. A run takes minutes, pulls container images
# and needs a working Docker - which is fine when you ask for it, and not fine on
# every commit.
#
# Usage:
#   just molecule                          # list roles that have a scenario
#   just molecule matrix-alertmanager-receiver
#   just molecule matrix-alertmanager-receiver converge   # any molecule subcommand
#
# Environment:
#   MOLECULE_DISTRO   base image to test on (default: ubuntu2604)

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
roles_dir="${repo_dir}/roles/custom"
venv_dir="${repo_dir}/var/molecule-venv"

list_roles() {
	find "${roles_dir}" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' \
		| while read -r candidate; do
			if [ -f "${roles_dir}/${candidate}/molecule/default/molecule.yml" ]; then
				echo "${candidate}"
			fi
		done \
		| sort
}

role="${1:-}"

if [ -z "${role}" ]; then
	echo "Roles with a Molecule scenario:"
	found="$(list_roles)"
	if [ -z "${found}" ]; then
		echo "  (none yet)"
	else
		printf '  %s\n' ${found}
	fi
	echo
	echo "Run one with: just molecule <role>"
	exit 0
fi

shift || true

if [ ! -f "${roles_dir}/${role}/molecule/default/molecule.yml" ]; then
	echo "No Molecule scenario at roles/custom/${role}/molecule/default" >&2
	echo >&2
	echo "Roles that have one:" >&2
	list_roles | sed 's/^/  /' >&2
	exit 1
fi

# The virtualenv lives under var/, which is gitignored, and is shared by every
# role - the dependencies are the same for all of them.
if [ ! -x "${venv_dir}/bin/molecule" ]; then
	echo "Creating the Molecule virtualenv in ${venv_dir/#$HOME/\~} ..."
	python3 -m venv "${venv_dir}"
	"${venv_dir}/bin/pip" install --quiet --upgrade pip
	"${venv_dir}/bin/pip" install --quiet -r "${repo_dir}/molecule-shared/requirements.txt"
fi

# Galaxy content is installed with `force: true` on every run, so two scenarios
# running at once will re-extract collections and roles into the same directory
# and pull them out from under each other mid-play. It shows up as a collection
# that was working moments earlier going missing:
#
#   the connection plugin 'community.docker.docker' was not found
#
# ANSIBLE_HOME relocates both `collections/` and `roles/`, so one variable is
# enough to give each role its own. The scenarios' ANSIBLE_ROLES_PATH follows it.
#
# Unset in CI, where it falls back to ~/.ansible - each role runs in its own job
# there, so there is nothing to collide with and nothing to gain from isolation.
export ANSIBLE_HOME="${ANSIBLE_HOME:-${repo_dir}/var/molecule-ansible-home/${role}}"

export MOLECULE_DISTRO="${MOLECULE_DISTRO:-ubuntu2604}"
export PY_COLORS="${PY_COLORS:-1}"
export ANSIBLE_FORCE_COLOR="${ANSIBLE_FORCE_COLOR:-1}"

echo "Running Molecule for ${role} on ${MOLECULE_DISTRO} ..."
cd "${roles_dir}/${role}"

if [ $# -eq 0 ]; then
	exec "${venv_dir}/bin/molecule" test --scenario-name default
fi

exec "${venv_dir}/bin/molecule" "$@" --scenario-name default
