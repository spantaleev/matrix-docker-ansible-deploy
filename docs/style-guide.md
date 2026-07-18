<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Style guide for playbook developers

This page describes the conventions used when developing this playbook and writing its documentation. Follow it when adding a new component (a role and its documentation page) or editing existing ones, so that everything stays consistent.

The guide is meant for anyone preparing a contribution, humans and AI agents alike. If you find existing files that deviate from it, feel free to send a pull request bringing them in line.

## Language

- Write in English, using American spelling ("customize", not "customise").
- Proper nouns are capitalized: Matrix, Element, Synapse, Ansible, Docker, Traefik, Postgres, Grafana, etc. Some projects deliberately brand themselves in lowercase (e.g. `baibot`, `rageshake`, `coturn`, `mautrix-telegram`) and keep their lowercase name even at the start of a sentence. When in doubt, follow the upstream project's own spelling.

## Markdown style

- Do not hard-wrap prose. Each paragraph is a single line in the source file, no matter how long. This keeps the source and the rendered result consistent and makes diffs and translations easier to work with.
- Number ordered lists sequentially (`1.`, `2.`, `3.`), instead of relying on the Markdown renderer to fix a repeated (`1.`, `1.`, `1.`) or wrong (`1.`, `2.`, `4.`) sequence.
- Use `-` for unordered lists.
- Wrap variable names, file paths, commands, domains, and service names in backticks (`` ` ``).
- Use fenced code blocks with a language hint (```` ```yaml ````, ```` ```sh ````) for configuration and command examples.
- Use relative links when linking between documentation pages (e.g. `[Configuring DNS](configuring-dns.md)`).
- Link to the upstream project's official documentation instead of duplicating its content (installation steps, distro-specific commands, etc.). Copied instructions go stale; links age much better.

## Example values

Use these placeholder values in documentation and code comments, so examples look the same everywhere:

| What | Value |
|------|-------|
| base domain | `example.com` |
| Matrix server domain | `matrix.example.com` |
| another (federated) server | `example.org` |
| user IDs | `@alice:example.com`, `@bob:example.com` |
| room ID | `!qporfwt:example.com` |
| room alias | `#room:example.com` |

The user and room ID values follow the examples in the [Matrix specification](https://spec.matrix.org/latest/#room-structure). Never use real domains, usernames, or tokens in examples.

Component-specific identifiers (e.g. a bridge bot like `@telegrambot:example.com`) are fine where they make an example clearer.

## Documentation page structure

Each component gets its own documentation page: `docs/configuring-playbook-<component>.md` (bridges use a `configuring-playbook-bridge-<name>.md` file name, bots use `configuring-playbook-bot-<name>.md`).

A typical page looks like this, with sections appearing in this order (sections that do not apply can be omitted):

```md
# Setting up ComponentName (optional)

The playbook can install and configure [ComponentName](https://github.com/example/component) for you.

See the project's [documentation](https://github.com/example/component/blob/main/README.md) to learn what it does and why it might be useful to you.

## Prerequisites (optional)

## Adjusting DNS records

## Adjusting the playbook configuration

### Extending the configuration

## Installing

## Usage

## Troubleshooting
```

Notes:

- Headings use sentence case ("Adjusting the playbook configuration", not "Adjusting The Playbook Configuration").
- The "Adjusting the playbook configuration" section tells people to add configuration to their `inventory/host_vars/matrix.example.com/vars.yml` file and shows a minimal `yaml` example.
- The "Installing" section references [playbook tags](playbook-tags.md) and shows the `just` command or `ansible-playbook` invocation to run.
- Look at an existing page for a similar component (another bridge, bot, or service) and copy its structure. The mautrix bridge pages share common sections via [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md), so bridge pages link there instead of repeating the shared content.

## Adding a new component

First, consider where the component belongs:

- Matrix-specific components are developed as roles in this repository, under `roles/custom/`.
- Components that are not Matrix-specific should live as external roles, preferably in the [MASH organization](https://github.com/mother-of-all-self-hosting/), and get wired into the playbook via `requirements.yml`.
- For components that are not Matrix-specific, also consider whether they belong in this Matrix playbook at all, or rather in [mash-playbook](https://github.com/mother-of-all-self-hosting/mash-playbook). Certain components (like Grafana or backup tools) are suitable for both playbooks. If something is too far away from general usefulness on a Matrix server, we prefer not to include it here, and to only have it in mash-playbook.

Besides the role itself and its documentation page, a new component touches a few other places. Make sure a pull request adding one covers all of them:

1. The role, in `roles/custom/matrix-<component>/` (or an external role wired via `requirements.yml`, as described above).
2. Role registration in `setup.yml`.
3. Wiring in `group_vars/matrix_servers`. Wire the component to the rest of the playbook there (referencing variables of other roles), but keep values that the role can construct by itself in the role's own `defaults/main.yml`.
4. The documentation page, `docs/configuring-playbook-<component>.md`, linked from the table of contents in `docs/README.md`.
5. An entry in the supported services list in `README.md`.
6. A row in `docs/container-images.md`, if the component runs a container.
7. A `CHANGELOG.md` entry announcing the new component.
8. License headers: every new file carries `SPDX-FileCopyrightText` and `SPDX-License-Identifier` comments, as this project follows the [REUSE](https://reuse.software/) specification.

Variable naming conventions:

- The variable prefix matches the role directory name: the `matrix-bridge-mautrix-telegram` role uses `matrix_bridge_mautrix_telegram_*` variables, the `matrix-bot-mjolnir` role uses `matrix_bot_mjolnir_*` variables, and so on.
- List-type variables that the playbook may extend automatically follow the `_auto` + `_custom` split: the main variable combines an `_auto` component (managed by the playbook via `group_vars`) and a `_custom` component (reserved for users). Where it makes sense, there is also a `_default` component, containing sensible defaults provided by the role itself. See `matrix_bridge_hookshot_container_additional_networks` and `matrix_bridge_hookshot_systemd_required_services_list` for examples.
- When a variable is renamed or removed, deprecate it so that people with stale configuration get told about it instead of it being silently ignored. Each role deprecates its own variables, in its `validate_config.yml` tasks. The `matrix_playbook_migration` role handles the cases a role cannot: variables of completely eliminated roles (which no longer have their own `validate_config.yml`), and validation that needs to run very early for some reason.
- For breaking changes that require the user's attention (beyond a renamed variable that validation already catches), bump `matrix_playbook_migration_expected_version` and add a matching entry to the `matrix_playbook_migration_breaking_changes` list (a summary and a `CHANGELOG.md` link), in `roles/custom/matrix_playbook_migration/defaults/main.yml`. Users declare `matrix_playbook_migration_validated_version` in their configuration, and the playbook walks them through all breaking changes between their validated version and the expected one. Also update the recommended value in `examples/vars.yml`; a pre-commit check enforces that it matches the expected version.
