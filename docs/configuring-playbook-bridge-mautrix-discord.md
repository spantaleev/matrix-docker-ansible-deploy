<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Hugues Morisset
SPDX-FileCopyrightText: 2021 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022 Abílio Costa
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Marko Weltzer
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Discord bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) and [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) bridges supported by the playbook.
- For using as a Bot we recommend the [Appservice Discord](configuring-playbook-bridge-appservice-discord.md), because it supports plumbing.
- For personal use with a discord account we recommend the `mautrix-discord` bridge (the one being discussed here), because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.

The playbook can install and configure [mautrix-discord](https://github.com/mautrix/discord) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/discord/index.html) to learn what it does and why it might be useful to you.

## Prerequisites

There are 2 ways to login to discord using this bridge, either by [scanning a QR code](#method-1-login-using-qr-code-recommended) using the Discord mobile app **or** by using a [Discord token](#method-2-login-using-discord-token-not-recommended).

If this is a dealbreaker for you, consider using one of the other Discord bridges supported by the playbook: [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) or [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md). These come with their own complexity and limitations, however, so we recommend that you proceed with this one if possible.

### Enable Appservice Double Puppet or Shared Secret Auth (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_discord_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: common relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@discordbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You can then follow instructions on the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/go/discord/authentication.html).

After logging in, the bridge will create portal rooms for some recent direct messages.

### Bridge guilds

If you'd like to bridge guilds, send `guilds status` to see the list of guilds, then send `guilds bridge GUILD_ID_HERE` for each guild that you'd like bridged. Make sure to replace `GUILD_ID_HERE` with the guild's ID.

After bridging, spaces will be created automatically, and rooms will be created if necessary when messages are received. You can also pass `--entire` to the bridge command to immediately create all rooms.

If you want to manually bridge channels, invite the bot to the room you want to bridge, and run `!discord bridge CHANNEL_ID_HERE` to bridge the room. Make sure to replace `CHANNEL_ID_HERE` with the channel's ID.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-discord`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_mautrix_discord_logging_level: 'debug'
```
