#!/bin/bash

# SPDX-FileCopyrightText: 2024 Slavi Pantaleev <slavi@devture.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# This script extracts translation templates (original English strings) into the `translation-templates/` directory.
# These templates are later used to generate locale files for each language in the `locales/` directory.
#
# By default `sphinx-build` extracts the templates into a `build/gettext` directory, while we'd like to have them in the `translation-templates/` directory.
# To avoid the `POT-Creation-Date` information in templates being updated every time we extract them,
# we restore the `translation-templates/` directory to the `build/gettext` directory before running the script.

set -euxo pipefail

base_path="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Restore the `translation-templates/` directory to the `build/gettext` directory
if [ -d ${base_path}/i18n/build ]; then
    rm -rf ${base_path}/i18n/build
fi
mkdir -p ${base_path}/i18n/build
cp -r ${base_path}/i18n/translation-templates ${base_path}/i18n/build/gettext

# Extract translation templates from the documentation into the `build/gettext` directory
sphinx-build -M gettext ${base_path} ${base_path}/i18n/build

# Clean up the build directory
rm -rf ${base_path}/i18n/build/gettext/.doctrees

# Update the `translation-templates/` directory with the new templates
if [ -d ${base_path}/i18n/translation-templates ]; then
    rm -rf ${base_path}/i18n/translation-templates
fi
mv ${base_path}/i18n/build/gettext ${base_path}/i18n/translation-templates

# Get rid of the `build` directory
rmdir ${base_path}/i18n/build
