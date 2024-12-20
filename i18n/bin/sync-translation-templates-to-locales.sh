#!/bin/bash

# This script updates the translation files (locales/<language>/**/*.po) for a given language.
# It uses the translation templates (translation-templates/**/*.pot) to generate the translation files.

set -euxo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <language>"
    exit 1
fi

LANGUAGE=$1

base_path="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ ! -f ${base_path}/i18n/translation-templates/README.pot ]; then
    echo "Translation templates not found. Please run the `extract-translation-templates.sh` script first."
    exit 1
fi

# Create necessary directories to avoid race conditions caused by
# Sphinx potentially trying to concurrently create them from separate threads below.
mkdir -p ${base_path}/i18n/locales/${LANGUAGE}/LC_MESSAGES/docs

# Update the translation files
sphinx-intl update \
    --pot-dir ${base_path}/i18n/translation-templates \
    --locale-dir ${base_path}/i18n/locales \
    --language ${LANGUAGE}
