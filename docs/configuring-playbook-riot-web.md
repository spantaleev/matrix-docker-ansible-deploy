<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Riot-web (optional)

By default, this playbook **used to install** the [Riot-web](https://github.com/element-hq/riot-web) Matrix client web application.

Riot has since been [renamed to Element](https://element.io/blog/welcome-to-element/).

- to learn more about Element Web and its configuration, see our dedicated [Configuring Element Web](configuring-playbook-client-element-web.md) documentation page
- to learn how to migrate from Riot to Element Web, see [Migrating to Element Web](#migrating-to-element-web) below

## Migrating to Element Web

### Migrating your custom settings

If you have custom `matrix_riot_web_` variables in your `inventory/host_vars/matrix.example.com/vars.yml` file, you'll need to rename them (`matrix_riot_web_` -> `matrix_client_element_`).

Some other playbook variables (but not all) with `riot` in their name are also renamed. The playbook checks and warns if you are using the old name for some commonly used ones.

### Domain migration

We used to set up Riot at the `riot.example.com` domain. The playbook now sets up Element Web at `element.example.com` by default.

There are a few options for handling this:

- (**avoiding changes** — using the old `riot.example.com` domain and avoiding DNS changes) — to keep using `riot.example.com` instead of `element.example.com`, override the domain at which the playbook serves Element Web: `matrix_server_fqn_element: "riot.{{ matrix_domain }}"`

- (**embracing changes** — using only `element.example.com`) — set up the `element.example.com` DNS record (see [Configuring DNS](configuring-dns.md)). You can drop the `riot.example.com` in this case.

### Re-running the playbook

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
