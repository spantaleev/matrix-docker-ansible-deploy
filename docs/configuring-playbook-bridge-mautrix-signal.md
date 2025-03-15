<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Hugues Morisset
SPDX-FileCopyrightText: 2020 - 2021 MDAD project contributors
SPDX-FileCopyrightText: 2020 Sabine Laszakovits
SPDX-FileCopyrightText: 2021 Julian Foad
SPDX-FileCopyrightText: 2021 Wolfgang Winter
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Marko Weltzer
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Benjamin Kampmann

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Signal bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-signal](https://github.com/mautrix/signal) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/signal/index.html) to learn what it does and why it might be useful to you.

## Prerequisites (optional)

### Prepare Postgres database on external Postgres server

If you're running with the Postgres database server integrated by the playbook (which is the default), you don't need to do anything special and can easily proceed with installing.

However, if you're [using an external Postgres server](configuring-playbook-external-postgres.md), you'd need to manually prepare a Postgres database for this bridge and adjust the variables related to that (`matrix_mautrix_signal_database_*`).

### Enable Appservice Double Puppet

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_signal_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@signalbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You can then follow instructions on the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/go/signal/authentication.html).

After logging in, the bridge will bridge chats as you receive messages.

**Note**: Signal does not support any kind of message history (even on official apps), so the bridge won't backfill any messages.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-signal`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_mautrix_signal_logging_level: 'debug'
```
