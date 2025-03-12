# SPDX-FileCopyrightText: 2024 Slavi Pantaleev <slavi@devture.com>
# SPDX-FileCopyrightText: 2024 Suguru Hirahara <acioustick@noreply.codeberg.org>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Configuration file for the Sphinx documentation builder.
# Also see the `i18n/` directory.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'matrix-docker-ansible-deploy'
copyright = '2018-%Y, Slavi Pantaleev, Aine Etke, MDAD community members'
author = 'Slavi Pantaleev, Aine Etke, MDAD community members'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

needs_sphinx = '8.1' # For the copyright year placeholder (%Y). Specified with pyproject.toml as well.

extensions = [
	'myst_parser',
	'sphinx_markdown_builder'
]
myst_gfm_only = True
myst_heading_anchors = 4 # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#auto-generated-header-anchors

master_doc = 'README'
source_suffix = {'.md': 'markdown'}

# Though the default config file advocates exclude_patterns, it is straightforward for us to use include_patterns to select directories explicitly.
include_patterns = [
	'docs/*',
	'i18n/README.md',
	'*.md',
]

locale_dirs = ['i18n/locales/']
gettext_compact = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']
