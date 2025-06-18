<!--
SPDX-FileCopyrightText: 2019 - 2022 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2022 Jim Myhrberg
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Discord bridging (optional)

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) and [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridges supported by the playbook.
- For using as a Bot we are recommend the Appservice Discord bridge (the one being discussed here), because it supports plumbing.
- For personal use we recommend the [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridge, because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.

The playbook can install and configure [matrix-appservice-discord](https://github.com/matrix-org/matrix-appservice-discord) for you.

See the project's [documentation](https://github.com/matrix-org/matrix-appservice-discord/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

Create a Discord Application [here](https://discordapp.com/developers/applications). Then retrieve Client ID, and create a bot from the Bot tab and retrieve the Bot token.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_discord_enabled: true
matrix_appservice_discord_client_id: "YOUR DISCORD APP CLIENT ID"
matrix_appservice_discord_bot_token: "YOUR DISCORD APP BOT TOKEN"

# As of Synapse 1.90.0, uncomment to enable the backwards compatibility (https://matrix-org.github.io/synapse/latest/upgrade#upgrading-to-v1900) that this bridge needs.
# Note: This deprecated method is considered insecure.
#
# matrix_synapse_configuration_extension_yaml: |
#   use_appservice_legacy_authorization: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-appservice-discord/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-appservice-discord/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_discord_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.


## Self-Service Bridging (Manual)

Self-service bridging allows you to bridge specific and existing Matrix rooms to specific Discord rooms. To enable it, add the following configuration to your `vars.yml` file:

```yaml
matrix_appservice_discord_bridge_enableSelfServiceBridging: true
```

**Note**: If self-service bridging is not enabled, `!discord help` commands will return no results.

### Usage

Once self-service is enabled, start a chat with `@_discord_bot:example.com` and say `!discord help bridge`.

Then, follow the instructions in the help output message.

If the bot is not already in the Discord server, follow the provided invite link. This may require you to be a administrator of the Discord server.

On the Discord side, send `!matrix help` to the bot to see the available commands for managing the bridge and Matrix users.

**Note**: Encrypted Matrix rooms are not supported as of writing.

## Portal Bridging (Automatic)

Through portal bridging, Matrix rooms will automatically be created by the bot and bridged to the relevant Discord room. This is done by simply joining a room with a specific name pattern (`#_discord_<guildID>_<channelID>`).

All Matrix rooms created this way are **listed publicly** by default, and you will not have admin permissions to change this. To get more control, [make yourself a room Administrator](#getting-administrator-access-in-a-portal-bridged-room). You can then unlist the room from the directory and change the join rules.

To disable portal bridging, add the following configuration to your `vars.yml` file:

```yaml
matrix_appservice_discord_bridge_disablePortalBridging: true
```

### Usage

To get started with Portal Bridging:

1. To invite the bot to Discord, retrieve the invite link from the `{{ matrix_appservice_discord_config_path }}/invite_link` file on the server (this defaults to `/matrix/appservice-discord/config/invite_link`). You need to peek at the file on the server via SSH, etc., because it's not available via HTTP(S).
2. Room addresses follow this syntax: `#_discord_<guildID>_<channelID>`. You can easily find the guild and channel IDs by logging into Discord in a browser and opening the desired channel. The URL will have this format: `discord.com/channels/<guildID>/<channelID>`.
3. Once you have figured out the appropriate room address, you can join by doing `/join #_discord_<guildID>_<channelID>` in your Matrix client.

## Getting Administrator access in a portal bridged room

By default, you won't have Administrator access in rooms created by the bridge.

To adjust room access privileges or do various other things (change the room name subsequently, etc.), you'd wish to become an Administrator.

There's the Discord bridge's guide for [setting privileges on bridge managed rooms](https://github.com/matrix-org/matrix-appservice-discord/blob/master/docs/howto.md#set-privileges-on-bridge-managed-rooms). To do the same with our container setup, run the following command on the server:

```sh
docker exec -it matrix-appservice-discord \
/bin/sh -c 'cp /cfg/registration.yaml /tmp/discord-registration.yaml && cd /tmp && node /build/tools/adminme.js -c /cfg/config.yaml -m "!qporfwt:example.com" -u "@alice:example.com" -p 100'
```

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-appservice-discord`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file (adapt to your needs) and re-run the playbook:

```yaml
matrix_appservice_discord_configuration_extension_yaml: |
  logging:
    # What level should the logger output to the console at.
    console: "info" # Valid values: silent, error, warn, http, info, verbose, silly
```
