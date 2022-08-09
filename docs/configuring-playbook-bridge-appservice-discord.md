# Setting up Appservice Discord (optional)

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) and [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridges supported by the playbook.   
- For using as a Bot we are recommend the Appservice Discord bridge (the one being discussed here), because it supports plumbing.  
- For personal use we recommend the [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridge, because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.

The playbook can install and configure [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) for you.

See the project's [documentation](https://github.com/Half-Shot/matrix-appservice-discord/blob/master/README.md) to learn what it does and why it might be useful to you.


## Setup Instructions

Instructions loosely based on [this](https://github.com/Half-Shot/matrix-appservice-discord#setting-up).

1. Create a Discord Application [here](https://discordapp.com/developers/applications).
2. Retrieve Client ID.
3. Create a bot from the Bot tab and retrieve the Bot token.
4. Enable the bridge with the following configuration in your `vars.yml` file:

```yaml
matrix_appservice_discord_enabled: true
matrix_appservice_discord_client_id: "YOUR DISCORD APP CLIENT ID"
matrix_appservice_discord_bot_token: "YOUR DISCORD APP BOT TOKEN"
```

5. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready.

Other configuration options are available via the `matrix_appservice_discord_configuration_extension_yaml` variable.

## Self-Service Bridging (Manual)

Self-service bridging allows you to bridge specific and existing Matrix rooms to specific Discord rooms. This is disabled by default, so it must be enabled by adding this to your `vars.yml`:

```yaml
matrix_appservice_discord_bridge_enableSelfServiceBridging: true
```

_Note: If self-service bridging is not enabled, `!discord help` commands will return no results._

Once self-service is enabled:

1. Start a chat with `@_discord_bot:<YOUR_DOMAIN>` and say `!discord help bridge`.
2. Follow the instructions in the help output message. If the bot is not already in the Discord server, follow the provided invite link. This may require you to be a administrator of the Discord server.

_Note: Encrypted Matrix rooms are not supported as of writing._

On the Discord side, you can say `!matrix help` to get a list of available commands to manage the bridge and Matrix users.

## Portal Bridging (Automatic)

Through portal bridging, Matrix rooms will automatically be created by the bot and bridged to the relevant Discord room. This is done by simply joining a room with a specific name pattern (`#_discord_<guildID>_<channlID>`).

All Matrix rooms created this way are **listed publicly** by default, and you will not have admin permissions to change this. To get more control, [make yourself a room Administrator](#getting-administrator-access-in-a-portal-bridged-room). You can then unlist the room from the directory and change the join rules.

If you want to disable portal bridging, set the following in `vars.yml`:

```yaml
matrix_appservice_discord_bridge_disablePortalBridging: true
```

To get started with Portal Bridging:

1. To invite the bot to Discord, retrieve the invite link from the `{{ matrix_appservice_discord_config_path }}/invite_link` file on the server (this defaults to `/matrix/appservice-discord/config/invite_link`). You need to peek at the file on the server via SSH, etc., because it's not available via HTTP(S).
2. Room addresses follow this syntax: `#_discord_<guildID>_<channelID>`. You can easily find the guild and channel IDs by logging into Discord in a browser and opening the desired channel. The URL will have this format: `discord.com/channels/<guildID>/<channelID>`.
3. Once you have figured out the appropriate room address, you can join by doing `/join #_discord_<guildID>_<channelID>` in your Matrix client.

## Getting Administrator access in a portal bridged room

By default, you won't have Administrator access in rooms created by the bridge.

To adjust room access privileges or do various other things (change the room name subsequently, etc.), you'd wish to become an Administrator.

There's the Discord bridge's guide for [setting privileges on bridge managed rooms](https://github.com/Half-Shot/matrix-appservice-discord/blob/master/docs/howto.md#set-privileges-on-bridge-managed-rooms). To do the same with our container setup, run the following command on the server:

```sh
docker exec -it matrix-appservice-discord \
/bin/sh -c 'cp /cfg/registration.yaml /tmp/discord-registration.yaml && cd /tmp && node /build/tools/adminme.js -c /cfg/config.yaml -m "!ROOM_ID:SERVER" -u "@USER:SERVER" -p 100'
```
