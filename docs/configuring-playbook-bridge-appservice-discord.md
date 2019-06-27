# Setting up Appservice Discord (optional)

The playbook can install and configure [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) for you.

See the project's [documentation](https://github.com/Half-Shot/matrix-appservice-discord/blob/master/README.md) to learn what it does and why it might be useful to you.

Setup Instructions:

loosely based on [this](https://github.com/Half-Shot/matrix-appservice-discord#setting-up)

1. Create a Discord Application [here](https://discordapp.com/developers/applications/me/create).
2. Retrieve Client ID and Bot token from this Application.
3. Enable the bridge with the following configuration in your `vars.yml` file:

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
