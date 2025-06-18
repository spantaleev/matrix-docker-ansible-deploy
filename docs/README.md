<!--
SPDX-FileCopyrightText: 2018 - 2021 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2019 Lyubomir Popov
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Table of Contents

## ⬇️ Installation guides <!-- NOTE: the 🚀 emoji is used by "Getting started" on README.md -->

There are two installation guides available for beginners and advanced users.

- ⚡ **[Quick start](quick-start.md) (for beginners)**: this is recommended for those who do not have an existing Matrix server and want to start quickly with "opinionated defaults".

- **Full installation guide (for advanced users)**: if you need to import an existing Matrix server's data into the new server or want to learn more while setting up the server, follow this guide.

    - [Prerequisites](prerequisites.md)

    - [Configuring DNS settings](configuring-dns.md)

    - [Getting the playbook](getting-the-playbook.md)

    - [Configuring the playbook](configuring-playbook.md)

    - [Installing](installing.md)

## 🛠️ Configuration options

<!--
NOTE:
- Avoid putting the same anchor links as configuring-playbook.md lists under the "configuration options" section. Note that most of them are linked to "configure-playbook-*.md" and their titles start with "Setting up" (e.g. "Setting up Hydrogen").
-->

You can check useful documentation for configuring components here: [Configuring the playbook](configuring-playbook.md)

- [Administration](configuring-playbook.md#administration) — services that help you in administrating and monitoring your Matrix installation

- [Authentication and user-related](configuring-playbook.md#authentication-and-user-related) — extend and modify how users are authenticated on your homeserver

- [Bots](configuring-playbook.md#bots) — bots provide various additional functionality to your installation

- [Bridges](configuring-playbook.md#bridging-other-networks) — bridges can be used to connect your Matrix installation with third-party communication networks

- [Clients](configuring-playbook.md#clients) — web clients for Matrix that you can host on your own domains

- [Core service adjustments](configuring-playbook.md#core-service-adjustments) — backbone of your Matrix system

- [File Storage](configuring-playbook.md#file-storage) — use alternative file storage to the default `media_store` folder

<!-- NOTE: sort list items above alphabetically -->

- [Other specialized services](configuring-playbook.md#other-specialized-services) — various services that don't fit any other categories

## 👨‍🔧 Maintenance

If your server and services experience issues, feel free to come to [our support room](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com) and ask for help.

<!-- NOTE: sort list items alphabetically -->

- [Maintenance and Troubleshooting](maintenance-and-troubleshooting.md)

- [PostgreSQL maintenance](maintenance-postgres.md)

- [Synapse maintenance](maintenance-synapse.md)

- [Upgrading services](maintenance-upgrading-services.md)

## Other documentation pages <!-- NOTE: this header's title and the section below need optimization -->

- ℹ️ **[FAQ](faq.md)** — various Frequently Asked Questions about Matrix, with a focus on this Ansible playbook

<!-- NOTE: sort list items under faq.md alphabetically -->

- [Alternative architectures](alternative-architectures.md)

- [Container images used by the playbook](container-images.md)

- [Obtaining an Access Token](obtaining-access-tokens.md)

- [Playbook tags](playbook-tags.md)

- [Registering users](registering-users.md)

- [Running `just` commands](just.md)

- [Self-building](self-building.md)

- [Uninstalling](uninstalling.md)

- [Updating users passwords](updating-users-passwords.md)

- [Using Ansible for the playbook](ansible.md)
