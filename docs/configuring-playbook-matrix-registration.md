<!--
SPDX-FileCopyrightText: 2020 - 2022 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up matrix-registration (optional)

> [!WARNING]
> - This is a poorly maintained and buggy project. It's better to avoid using it.
> - This is not related to [matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md)

The playbook can install and configure [matrix-registration](https://github.com/ZerataX/matrix-registration) for you. It is a simple python application to have a token based Matrix registration.

Use matrix-registration to **create unique registration links**, which people can use to register on your Matrix server. It allows certain people (these having a special link) to register a user account, **keeping your server's registration closed (private)**.

**matrix-registration** provides 2 things:

- **an API for creating registration tokens** (unique registration links). This API can be used via `curl` or via the playbook (see [Usage](#usage) below)

- **a user registration page**, where people can use these registration tokens. By default, exposed at `https://matrix.example.com/matrix-registration`

## Adjusting DNS records (optional)

By default, this playbook installs the matrix-registration on the `matrix.` subdomain, at the `/matrix-registration` path (https://matrix.example.com/matrix-registration). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-matrix-registration-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable matrix-registration, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_registration_enabled: true

# Generate a strong secret here. You can create one with a command like `pwgen -s 64 1`.
matrix_registration_admin_secret: "ENTER_SOME_SECRET_HERE"
```

### Adjusting the matrix-registration URL (optional)

By tweaking the `matrix_registration_hostname` and `matrix_registration_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_registration_hostname: registration.example.com
matrix_registration_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the matrix-registration domain (`registration.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-registration/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-registration/templates/config.yaml.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_registration_configuration_extension_yaml` variable

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

**matrix-registration** gets exposed at `https://matrix.example.com/matrix-registration`

It provides various [APIs](https://github.com/ZerataX/matrix-registration/wiki/api) — for creating registration tokens, listing tokens, disabling tokens, etc. To make use of all of its capabilities, consider using `curl`.

We make the most common APIs easy to use via the playbook (see below).

### Creating registration tokens

To **create a new user registration token (link)**, use this command:

```sh
ansible-playbook -i inventory/hosts setup.yml \
--tags=generate-matrix-registration-token \
--extra-vars="one_time=yes ex_date=2021-12-31"
```

The above command creates and returns a **one-time use** token, which **expires** on the 31st of December 2021. Adjust the `one_time` and `ex_date` variables as you see fit.

Share the unique registration link (generated by the command above) with users to let them register on your Matrix server.

### Listing registration tokens

To **list the existing user registration tokens**, use this command:

```sh
ansible-playbook -i inventory/hosts setup.yml \
--tags=list-matrix-registration-tokens
```

The shortcut command with `just` program is also available: `just run-tags list-matrix-registration-tokens`

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-registration`.
