# Setting up Appservice Discord (optional)

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

4. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready.
5. Retrieve Discord invite link from the `{{ matrix_appservice_discord_config_path }}/invite_link` file on the server (this defaults to `/matrix/appservice-discord/config/invite_link`)
6. Invite the Bot to Discord servers you wish to bridge. Administrator permission is recommended.
7. Join the rooms by following this syntax `#_discord_guildid_channelid` - can be easily retrieved by logging into Discord in a browser and opening the desired channel. URL will have this format: `discordapp.com/channels/guild_id/channel_id`

Other configuration options are available via the `matrix_appservice_discord_configuration_extension_yaml` variable.


## Getting Administrator access in a room

By default, you won't have Administrator access in rooms created by the bridge.

To [adjust room access privileges](#adjusting-room-access-privileges) or do various other things (change the room name subsequently, etc.), you'd wish to become an Administrator.

There's the Discord bridge's guide for [setting privileges on bridge managed rooms](https://github.com/Half-Shot/matrix-appservice-discord/blob/master/docs/howto.md#set-privileges-on-bridge-managed-rooms). To do the same with our container setup, run the following command on the server:

```
docker exec -it matrix-appservice-discord /bin/sh -c 'cp /build/tools/adminme.js /tmp/adminme.js && cp /cfg/registration.yaml /tmp/discord-registration.yaml && cd /tmp && node /tmp/adminme.js -c /cfg/config.yaml -r "!ROOM_ID:SERVER" -u "@USER:SERVER" -p 100'
```


## Adjusting room access privileges

All rooms created by the bridge are **listed publicly** in your server's directory and **joinable by everyone** by default.

To get more control of them, [make yourself a room Administrator](#getting-administrator-access-in-a-room) first.

You can then unlist the room from the directory and change the join rules.
