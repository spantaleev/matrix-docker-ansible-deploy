<!--
SPDX-FileCopyrightText: 2024 Slavi Pantaleev <slavi@devture.com>
SPDX-FileCopyrightText: 2024 Suguru Hirahara <acioustick@noreply.codeberg.org>

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Internationalization

Translated documentation files are published and maintained in [`translations/`](translations/) directory.

Currently, we support translation of:

- Markdown files found at the top level project directory
- Markdown files found in the [`docs`](../docs/) directory (this is where the bulk of the documentation is)
- this current document in the `i18n` directory

💡 For readers' sake, we only [publish translations in a new language](#publish-translations-in-a-new-language) when the translation progresses beyond a certain threshold (requiring that at least the project README and core installation guides are translated).

Organization of this `i18n` directory is as follows:

- [PUBLISHED_LANGUAGES](PUBLISHED_LANGUAGES): a list of languages that we publish translations for (in the [translations/](translations/) directory)
- [.gitignore](.gitignore): a list of files and directories to ignore in the `i18n` directory. We intentionally ignore translated results (`translations/<language>` directories) for languages that are still in progress. We only [publish translations in a new language](#publish-translations-in-a-new-language) when the translation progresses beyond a certain threshold.
- [justfile](justfile): a list of recipes for [just](https://github.com/casey/just) command runner
- [requirements.txt](requirements.txt): a list of Python packages required to work with translations
- [translation-templates/](translation-templates/): a list of English translation templates - strings extracted from Markdown files
- [locales/](locales/): localization files for languages
- [translations/](translations/): translated documents for published languages (see [PUBLISHED_LANGUAGES](PUBLISHED_LANGUAGES) and [publish translations in a new language](#publish-translations-in-a-new-language))

## Guide for translators

This project uses [Sphinx](https://www.sphinx-doc.org/) to generate translated documents.

For details about using Sphinx for translation, refer [this official document](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html) as well.

For now, translations are handled manually by editing `.po` files in the `locales/<language>` directory. In the future, we plan on integrating with [Weblate](https://weblate.org/) to allow for translating from a web interface.

### (Recommended) Using the uv package manager and just command runner

If you have the [uv](https://docs.astral.sh/uv/) package manager and [just](https://github.com/casey/just) command runner installed, you can use our [justfile](justfile) recipes to easily manage translation files and build translated documents.

The recipes will use [uv](https://github.com/astral-sh/uv) to auto-create [a Python virtual environment](https://docs.astral.sh/uv/pip/environments/) in the `.venv` directory and install the required Python packages (as per [requirements.txt](requirements.txt)) to it.

#### Preparation

Make sure you have the [uv](https://docs.astral.sh/uv/) package manager and [just](https://github.com/casey/just) command runner installed.

#### Translation

Recommended flow when working on a new language (replace `<language>` with the language code, e.g. `bg`):

- Update the locale files for your language: `just sync-for-language <language>` (internally, this automatically runs `just extract-translation-templates` to make sure the translation templates are up-to-date)

- Use an editor to translate the files in the `locales/<language>` directory

- Build translated documents: `just build-for-language <language>`

- Preview the result in the `translations/<language>` directory

- Commit your changes done to the `locales/<language>` directory

- If you have progressed with the translation beyond a certain threshold, consider [Publishing translations in a new language](#publish-translations-in-a-new-language)

### Using any other package manager and manual scripts

If you cannot use [uv](https://docs.astral.sh/uv/) and/or [just](https://github.com/casey/just), you can:

- manage Python packages in another way ([pip](https://pip.pypa.io/en/stable/), [Poetry](https://python-poetry.org/), etc.)
- manage translation strings and build translated documents manually by invoking scripts from the [bin](bin/) directory

#### Preparation

##### virtualenv and pip

- Create a Python virtual environment in the `.venv` directory: `virtualenv .venv`
- Activate the virtual environment: `source .venv/bin/activate`
- Install the required Python packages using [pip](https://pip.pypa.io/en/stable/): `pip install -r requirements.txt`

#### Translation

Recommended flow when working on a new language (replace `<language>` with the language code, e.g. `bg`):

- Ensure the English translation templates ([translation-templates/](translation-templates/)) are extracted: `./bin/extract-translation-templates.sh`

- Update the locale files for your language: `./bin/sync-translation-templates-to-locales.sh <language>`

- Use an editor to translate the files in the `locales/<language>` directory

- Build translated documents: `./bin/build-translated-result.sh <language>`

- Preview the result in the `translations/<language>` directory

- Commit your changes done to the `locales/<language>` directory

- If you have progressed with the translation beyond a certain threshold, consider [Publishing translations in a new language](#publish-translations-in-a-new-language)

### Publish translations in a new language

To publish prebuilt documents translated in a new language to the `translations/<language>` directory:

- add its language code to the [PUBLISHED_LANGUAGES](PUBLISHED_LANGUAGES) file
- whitelist its `translations/<language>` directory by adding a `!translations/<language>` rule to the [.gitignore](.gitignore) file

💡 Leave a trailing new line at the end of the [PUBLISHED_LANGUAGES](PUBLISHED_LANGUAGES) file.
