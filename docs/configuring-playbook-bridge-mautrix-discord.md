<!--
SPDX-FileCopyrightText: 2018 Hugues Morisset
SPDX-FileCopyrightText: 2018-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021, 2022 MDAD project contributors
SPDX-FileCopyrightText: 2022 Abílio Costa
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Marko Weltzer
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Discord bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) bridge supported by the playbook.

The playbook can install and configure [mautrix-discord](https://github.com/mautrix/discord) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/discord/index.html) to learn what it does and why it might be useful to you.

## Prerequisites

There are 3 ways to login to discord using this bridge, either by [scanning a QR code](https://docs.mau.fi/bridges/go/discord/authentication.html#qr-login) using the Discord mobile app, by using a [Discord token](https://docs.mau.fi/bridges/go/discord/authentication.html#token-login), **or** by using a [Discord bot token](https://docs.mau.fi/bridges/go/discord/authentication.html#bot-token-login).

⚠️ QR code login is considered a self-bot and is forbidden by Discord. It can result in an account termination. See the [Discord policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots).

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

### Enable relay

The bridge supports using Discord's webhook feature to relay messages from Matrix users who haven't logged into the bridge.

In a room that has already been bridged, run `!discord set-relay --create`. The bridge will then create a webhook in the bridged discord channel and begin relaying messages. If the discord user does not have access to manage webhooks, run `!discord set-relay --url <url>` with the url of an already created webhook. (See Discords [Intro to webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))

More information on relaying is available on the [official documentation](https://docs.mau.fi/bridges/go/discord/relay.html).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-discord`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_mautrix_discord_logging_level: 'debug'
```

### Command requires room admin rights when user is creator

[MSC4289](https://github.com/matrix-org/matrix-spec-proposals/blob/main/proposals/4289-privilege-creators.md), introduced in [room version 12](https://spec.matrix.org/unstable/rooms/v12/), gives creators an infinitley high powerlevel. At the time of implementation, mautrix-discord and similar applications may not identify creators as or above admins. Either a separate admin user will need to manage the bridge or the room version should be less than version 12.
