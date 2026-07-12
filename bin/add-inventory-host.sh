#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 MDAD project contributors
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Adds a new host to the inventory, based on the example files in `examples/`:
# - creates `inventory/hosts` (or adds the host to it, if it already exists)
# - creates `inventory/host_vars/matrix.DOMAIN/vars.yml` with strong secrets generated automatically
#
# Existing configuration for the same host is never overwritten - the script refuses to run instead.
#
# Usage: bin/add-inventory-host.sh <base-domain> <server-address>
#
# - <base-domain> is the base domain (`example.com`), not the Matrix server hostname (`matrix.example.com`)
# - <server-address> is the server's external IP address or domain name

set -euo pipefail

base_path="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ $# -ne 2 ]; then
	echo "Usage: $0 <base-domain> <server-address>" >&2
	echo "Example: $0 example.com 1.2.3.4" >&2
	exit 1
fi

domain="$1"
server_address="$2"

if ! printf '%s' "${domain}" | grep -Eq '^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)+$'; then
	echo "Error: '${domain}' does not look like a valid domain name" >&2
	exit 1
fi

if ! printf '%s' "${server_address}" | grep -Eq '^[A-Za-z0-9.:_-]+$'; then
	echo "Error: '${server_address}' does not look like a valid server address (IP address or domain name)" >&2
	exit 1
fi

case "${domain}" in
	matrix.*)
		echo "Warning: you likely need to pass your base domain (example.com), not the Matrix server hostname (matrix.example.com)." >&2
		echo "Proceeding anyway. Your Matrix server hostname will be: matrix.${domain}" >&2
		;;
esac

matrix_hostname="matrix.${domain}"
hosts_file="${base_path}/inventory/hosts"
vars_dir="${base_path}/inventory/host_vars/${matrix_hostname}"
vars_file="${vars_dir}/vars.yml"
hosts_entry="${matrix_hostname} ansible_host=${server_address} ansible_ssh_user=root"

if [ -e "${vars_dir}" ]; then
	echo "Error: ${vars_dir} already exists. Refusing to overwrite it." >&2
	exit 1
fi

if [ -f "${hosts_file}" ]; then
	if ! grep -q '^\[matrix_servers\]' "${hosts_file}"; then
		echo "Error: ${hosts_file} exists, but does not contain a [matrix_servers] section." >&2
		echo "Unrecognized inventory format. Add the host to it manually:" >&2
		echo "${hosts_entry}" >&2
		exit 1
	fi

	matrix_hostname_pattern="$(printf '%s' "${matrix_hostname}" | sed 's|\.|\\.|g')"
	if grep -Eq "^${matrix_hostname_pattern}([[:space:]]|$)" "${hosts_file}"; then
		echo "Error: ${hosts_file} already contains an entry for ${matrix_hostname}. Refusing to modify it." >&2
		exit 1
	fi
fi

generate_secret() {
	if command -v pwgen >/dev/null 2>&1; then
		pwgen -s 64 1
	elif command -v openssl >/dev/null 2>&1; then
		openssl rand -base64 192 | LC_ALL=C tr -dc 'A-Za-z0-9' | head -c 64
	else
		head -c 4096 /dev/urandom | LC_ALL=C tr -dc 'A-Za-z0-9' | head -c 64
	fi
}

generic_secret_key="$(generate_secret)"
postgres_password="$(generate_secret)"

for secret in "${generic_secret_key}" "${postgres_password}"; do
	if [ "${#secret}" -lt 64 ]; then
		echo "Error: failed to generate a secret" >&2
		exit 1
	fi
done

mkdir -p "${vars_dir}"

sed \
	-e "s|^matrix_domain:.*|matrix_domain: ${domain}|" \
	-e "s|^matrix_homeserver_generic_secret_key:.*|matrix_homeserver_generic_secret_key: '${generic_secret_key}'|" \
	-e "s|^postgres_connection_password:.*|postgres_connection_password: '${postgres_password}'|" \
	"${base_path}/examples/vars.yml" > "${vars_file}"

if [ -f "${hosts_file}" ]; then
	# Insert the new host right after the [matrix_servers] section header.
	hosts_file_tmp="$(mktemp "${hosts_file}.XXXXXX")"
	awk -v entry="${hosts_entry}" '{print} $0 ~ /^\[matrix_servers\]/ && !done {print entry; done=1}' \
		"${hosts_file}" > "${hosts_file_tmp}"
	mv "${hosts_file_tmp}" "${hosts_file}"
else
	sed \
		-e "s|^matrix\.example\.com .*|${hosts_entry}|" \
		"${base_path}/examples/hosts" > "${hosts_file}"
fi

echo "Added host ${matrix_hostname} to the inventory:"
echo "- ${hosts_file}"
echo "- ${vars_file}"
echo ""
echo "Secrets were generated automatically for matrix_homeserver_generic_secret_key and postgres_connection_password."
echo "Review and adjust these files before installing."
