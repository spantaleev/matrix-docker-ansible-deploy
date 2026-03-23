#!/bin/bash

# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Ensures that the migration validated version in examples/vars.yml
# matches the expected version in the matrix_playbook_migration role defaults.

set -euo pipefail

defaults_file="roles/custom/matrix_playbook_migration/defaults/main.yml"
examples_file="examples/vars.yml"

expected_version=$(grep -oP '^matrix_playbook_migration_expected_version:\s*"?\K[^"]+' "$defaults_file")
examples_version=$(grep -oP '^matrix_playbook_migration_validated_version:\s*"?\K[^"]+' "$examples_file")

if [ -z "$expected_version" ]; then
	echo "ERROR: Could not extract matrix_playbook_migration_expected_version from $defaults_file"
	exit 1
fi

if [ -z "$examples_version" ]; then
	echo "ERROR: Could not extract matrix_playbook_migration_validated_version from $examples_file"
	exit 1
fi

if [ "$expected_version" != "$examples_version" ]; then
	echo "ERROR: Migration version mismatch!"
	echo "  $defaults_file has expected version: $expected_version"
	echo "  $examples_file has validated version: $examples_version"
	echo ""
	echo "Please update $examples_file to match."
	exit 1
fi
