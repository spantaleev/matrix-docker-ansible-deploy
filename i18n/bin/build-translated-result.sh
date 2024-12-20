#!/bin/bash

# SPDX-FileCopyrightText: 2024 Slavi Pantaleev <slavi@devture.com>
# SPDX-FileCopyrightText: 2024 Suguru Hirahara <acioustick@noreply.codeberg.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# This script builds the translated result (translated project) for a given language in the `translations/<language>/` directory.

set -euxo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <language>"
    exit 1
fi

LANGUAGE=$1

base_path="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ ! -f ${base_path}/i18n/locales/${LANGUAGE}/LC_MESSAGES/README.po ]; then
    echo "Locales for ${LANGUAGE} not found. Please run the `sync-translation-templates-to-locales.sh` script first."
    exit 1
fi

# Prepare a clean build directory
if [ -d ${base_path}/i18n/translated-result-build-${LANGUAGE} ]; then
    rm -rf ${base_path}/i18n/translated-result-build-${LANGUAGE}
fi
mkdir -p ${base_path}/i18n/translated-result-build-${LANGUAGE}

# Build the translated documentation
sphinx-build \
    -b markdown \
    -D language="${LANGUAGE}" \
    ${base_path}/ \
    ${base_path}/i18n/translated-result-build-${LANGUAGE}

# Clean up .mo files produced during the build.
# We don't commit them to the repository anyway, so they can be left alone,
# but we'd rather keep things clean anyway.
find ${base_path}/i18n/locales/${LANGUAGE} -type f -name '*.mo' -delete

# Clean up the build directory
rm -rf ${base_path}/i18n/translated-result-build-${LANGUAGE}/.doctrees

# Copy assets
cp -r ${base_path}/docs/assets ${base_path}/i18n/translated-result-build-${LANGUAGE}/docs/assets/

# Remove the old result directory for this language
if [ -d ${base_path}/i18n/translations/${LANGUAGE} ]; then
    rm -rf ${base_path}/i18n/translations/${LANGUAGE}
fi

# Make sure the `translations/` directory exists
if [ ! -d ${base_path}/i18n/translations ]; then
    mkdir -p ${base_path}/i18n/translations
fi

# Relocate the built result to translations/<language>
mv ${base_path}/i18n/translated-result-build-${LANGUAGE} ${base_path}/i18n/translations/${LANGUAGE}
