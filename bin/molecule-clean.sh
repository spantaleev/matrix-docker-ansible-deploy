#!/bin/bash
# Removes what `just molecule` leaves under var/.
#
# Called through `just molecule-clean [--idle-days N]`.
#
# Two things accumulate. The per-role Ansible homes are ~7 MB each and are
# rewritten on every run rather than growing, so they are bounded by the number
# of roles that have a scenario. The shared virtualenv is the bulk of it (over
# 500 MB) and is recreated on the next run, which costs a pip install.
#
# Usage:
#   just molecule-clean                  # everything, after showing what and how much
#   just molecule-clean --idle-days 14   # only what has not been touched in 14 days
#   just molecule-clean --yes            # skip the confirmation
#
# --idle-days is what makes this safe to run unattended: a scenario you ran this
# morning keeps its cache, and only roles you have not touched in a while lose
# theirs.

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
var_dir="${repo_dir}/var"

idle_days=""
assume_yes="false"

while [ $# -gt 0 ]; do
	case "$1" in
		--idle-days)
			idle_days="${2:-}"
			if ! [[ "${idle_days}" =~ ^[0-9]+$ ]]; then
				echo "--idle-days needs a whole number of days" >&2
				exit 1
			fi
			shift 2
			;;
		--yes|-y)
			assume_yes="true"
			shift
			;;
		*)
			echo "Unknown argument: $1" >&2
			echo "Usage: just molecule-clean [--idle-days N] [--yes]" >&2
			exit 1
			;;
	esac
done

# Only ever the two directories bin/molecule.sh creates, named explicitly. `var/`
# holds other things and must never be removed wholesale.
targets=()
for candidate in "${var_dir}/molecule-ansible-home" "${var_dir}/molecule-venv"; do
	[ -d "${candidate}" ] || continue

	if [ -n "${idle_days}" ] && [ -z "$(find "${candidate}" -maxdepth 0 -mtime "+${idle_days}")" ]; then
		continue
	fi

	targets+=("${candidate}")
done

if [ ${#targets[@]} -eq 0 ]; then
	if [ -n "${idle_days}" ]; then
		echo "Nothing idle for more than ${idle_days} day(s)."
	else
		echo "Nothing to clean."
	fi
	exit 0
fi

echo "Would remove:"
for target in "${targets[@]}"; do
	printf '  %s  %s\n' "$(du -sh "${target}" | cut -f1)" "${target/#$HOME/\~}"
done

if [ "${assume_yes}" != "true" ]; then
	read -r -p "Remove these? [y/N] " reply
	case "${reply}" in
		y|Y|yes|YES) ;;
		*) echo "Left alone."; exit 0 ;;
	esac
fi

for target in "${targets[@]}"; do
	rm -rf "${target}"
	echo "Removed ${target/#$HOME/\~}"
done

echo "The virtualenv is recreated on the next \`just molecule\` run."
