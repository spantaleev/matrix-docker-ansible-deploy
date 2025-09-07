<!--
SPDX-FileCopyrightText: 2018 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2018 Aaron Raimist
SPDX-FileCopyrightText: 2019 Edgars Voroboks
SPDX-FileCopyrightText: 2019 Michael Haak
SPDX-FileCopyrightText: 2020 Kevin Lanni
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Mitja Jež
SPDX-FileCopyrightText: 2024 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Installing

<sup>[Prerequisites](prerequisites.md) > [Configuring DNS settings](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > [Configuring the playbook](configuring-playbook.md) > Installing</sup>

If you've configured your DNS records and the playbook, you can start the installation procedure.

## Update Ansible roles

Before installing, you need to update the Ansible roles that this playbook uses and fetches from outside.

To update your playbook directory and all upstream Ansible roles (defined in the `requirements.yml` file), run:

- either: `just update`
- or: a combination of `git pull` and `just roles` (or `make roles` if you have `make` program on your computer instead of `just`)

If you don't have either `just` tool or `make` program, you can run the `ansible-galaxy` tool directly: `rm -rf roles/galaxy; ansible-galaxy install -r requirements.yml -p roles/galaxy/ --force`

For details about `just` commands, take a look at: [Running `just` commands](just.md).

## Install Matrix server and services

The Ansible playbook's tasks are tagged, so that certain parts of the Ansible playbook can be run without running all other tasks.

The general command syntax for installation (and also maintenance) is: `ansible-playbook -i inventory/hosts setup.yml --tags=COMMA_SEPARATED_TAGS_GO_HERE`. It is recommended to get yourself familiar with the [playbook tags](playbook-tags.md) before proceeding.

If you **don't** use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the all Ansible commands.

If you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to all Ansible commands.

There 2 ways to start the installation process — depending on whether you're [Installing a brand new server (without importing data)](#installing-a-brand-new-server-without-importing-data) or [Installing a server into which you'll import old data](#installing-a-server-into-which-youll-import-old-data).

**Note**: if you are migrating from an old server to a new one, take a look at [this guide](maintenance-migrating.md) instead. This is an easier and more straightforward way than installing a server and importing old data into it.

### Installing a brand new server (without importing data)

If this is **a brand new** Matrix server and you **won't be importing old data into it**, run all these tags:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,ensure-matrix-users-created,start
```

This will do a full installation and start all Matrix services.

**Note**: if the command does not work as expected, make sure that you have properly installed and configured software required to run the playbook, as described on [Prerequisites](prerequisites.md).

### Installing a server into which you'll import old data

If you will be importing data into your newly created Matrix server, install it, but **do not** start its services just yet. Starting its services or messing with its database now will affect your data import later on.

To do the installation **without** starting services, run `ansible-playbook` with the `install-all` tag only:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all
```

> [!WARNING]
> Do not run the just "recipe" `just install-all` instead, because it automatically starts services at the end of execution. See: [Difference between playbook tags and shortcuts](just.md#difference-between-playbook-tags-and-shortcuts)

When this command completes, services won't be running yet.

You can now:

- [Importing an existing SQLite database (from another Synapse installation)](importing-synapse-sqlite.md) (optional)

- [Importing an existing Postgres database (from another installation)](importing-postgres.md) (optional)

- [Importing `media_store` data files from an existing Synapse installation](importing-synapse-media-store.md) (optional)

… and then proceed to starting all services:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=ensure-matrix-users-created,start
```

## Create your user account

ℹ️ *You can skip this step if you have installed a server and imported old data to it.*

As you have configured your brand new server and the client, you need to **create your user account** on your Matrix server.

After creating the user account, you can log in to it with [Element Web](configuring-playbook-client-element-web.md) that this playbook has installed for you at this URL: `https://element.example.com/`.

To create your user account (as an administrator of the server) via this Ansible playbook, run the command below on your local computer.

**Notes**:
- Make sure to adjust `YOUR_USERNAME_HERE` and `YOUR_PASSWORD_HERE`
- For `YOUR_USERNAME_HERE`, use a plain username like `alice`, not your full ID (`@alice:example.com`)
- Use `admin=yes` to make your user account an administrator of the Matrix server

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=YOUR_USERNAME_HERE password=YOUR_PASSWORD_HERE admin=yes' --tags=register-user

# Example: ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=alice password=secret-password admin=yes' --tags=register-user
```

Feel free to create as many accounts (for friends, family, etc.) as you want. Still, perhaps you should grant full administrative access to your account only (with `admin=yes`), and others should be created with `admin=no`.

For more information, see the documentation for [registering users](registering-users.md).

## Finalize the installation

Now you've configured Matrix services and your user account, you need to **finalize the installation process** by [setting up Matrix delegation (redirection)](howto-server-delegation.md), so that your Matrix server (`matrix.example.com`) can present itself as the base domain (`example.com`) in the Matrix network.

This is required for federation to work! Without a proper configuration, your server will effectively not be part of the Matrix network.

To configure the delegation, you have these two options. Choose one of them according to your situation.

- If you can afford to point the base domain at the Matrix server, follow the instructions below which guide you into [serving the base domain](configuring-playbook-base-domain-serving.md) from the integrated web server. It will enable you to use a Matrix user ID like `@alice:example.com` while hosting services on a subdomain like `matrix.example.com`.
- Alternatively, if you're using the base domain for other purposes and cannot point it to the Matrix server (and thus cannot "serve the base domain" from it), you most likely need to [manually install well-known files on the base domain's server](configuring-well-known.md#manually-installing-well-known-files-on-the-base-domains-server), but feel free to familiarize yourself with all [server delegation (redirection) options](howto-server-delegation.md).

To have the base domain served from the integrated web server, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_static_files_container_labels_base_domain_enabled: true
```

After configuring the playbook, run the command below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-matrix-static-files,start
```

**If an error is not returned, the installation has completed and the services have been started successfully**🎉

## Things to do next

After completing the installation, you can:

- [check if services work](maintenance-and-troubleshooting.md#how-to-check-if-services-work)
- or [set up additional services](configuring-playbook.md#other-configuration-options) (bridges to other chat networks, bots, etc.)
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or learn how to [maintain your server](faq.md#maintenance)
- or join some Matrix rooms:
  * via the *Explore rooms* feature in Element Web or some other clients, or by discovering them using this [matrix-static list](https://view.matrix.org). **Note**: joining large rooms may overload small servers.
  * or come say Hi in our support room — [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com). You might learn something or get to help someone else new to Matrix hosting.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/s.pantaleev/donate))

### ⚠️ Keep the playbook and services up-to-date

While this playbook helps you to set up Matrix services and maintain them, it will **not** automatically run the maintenance task for you. You will need to update the playbook and re-run it **manually**.

The upstream projects, which this playbook makes use of, occasionally if not often suffer from security vulnerabilities.

Since it is unsafe to keep outdated services running on the server connected to the internet, please consider to update the playbook and re-run it periodically, in order to keep the services up-to-date.

Also, do not forget to update your system regularly. While this playbook may install basic services, such as Docker, it will not interfere further with system maintenance. Keeping the system itself up-to-date is out of scope for this playbook.

For more information about upgrading or maintaining services with the playbook, take a look at this page: [Upgrading the Matrix services](maintenance-upgrading-services.md)

Feel free to **re-run the setup command any time** you think something is wrong with the server configuration. Ansible will take your configuration and update your server to match.

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Note**: see [this page on the playbook tags](playbook-tags.md) for more information about those tags.

### Make full use of `just` shortcut commands

After you get familiar with reconfiguring and re-running the playbook to maintain the server, upgrade its services, etc., you probably would like to make use of `just` shortcut commands for faster input.

For example, `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

You can learn about the shortcut commands on this page: [Running `just` commands](just.md)
