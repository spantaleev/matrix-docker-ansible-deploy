<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Guidance for AI agents

This file gives AI coding agents the minimum context for working on this repository. Human contributors may find it a useful summary too.

## What this is

An Ansible playbook that installs and manages a Matrix homeserver and dozens of related services, each running as a Docker container wrapped in a systemd service.

## Layout

- `setup.yml`: the main playbook, listing all roles.
- `roles/custom/`: roles maintained in this repository.
- `roles/galaxy/`: external roles, downloaded according to `requirements.yml` via [agru](https://github.com/etkecc/agru) (preferred) or `ansible-galaxy`. Run `just roles` to install them (or `just update` to also pull the playbook itself). Editing these roles locally is fine while preparing or testing a fix, but the changes get wiped on the next roles update, so they must be synced back to the role's upstream repository, followed by a version pin update in `requirements.yml`.
- `group_vars/matrix_servers`: wires roles together (feeding one role's variables into another). Values a role can construct by itself belong in the role's `defaults/main.yml`, not here.
- `docs/`: user-facing documentation, one page per component.
- `i18n/`: translation infrastructure. Do not edit locale files by hand; they are managed by automation.
- `CHANGELOG.md`: user-facing announcements, newest first.

## Conventions

Follow the [style guide for playbook developers](docs/style-guide.md). In particular:

- Variable prefixes match the role directory name.
- Playbook-extensible list variables use the `_auto` + `_custom` split; `_custom` is reserved for users.
- Renamed or removed variables get a validation entry, so stale user configuration produces an error instead of being silently ignored. Each role deprecates its own variables in its `validate_config.yml`; the `matrix_playbook_migration` role covers eliminated roles and very-early validation, and also gates breaking changes via `matrix_playbook_migration_expected_version` (see the style guide).
- Every file carries SPDX license headers ([REUSE](https://reuse.software/) specification).
- New components must be registered in `setup.yml`, `group_vars/matrix_servers`, `docs/README.md`, `README.md`, `docs/container-images.md`, and get a `CHANGELOG.md` entry.

## Other notes

- Documentation examples use `example.com`, `@alice:example.com`, and the other placeholder values listed in the style guide.
- Write role tasks concurrency-safe: use `ansible.builtin.tempfile` for temporary files (removed in an `always` block), never fixed shared paths.
- One logical change per commit.
