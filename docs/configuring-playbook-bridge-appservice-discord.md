# Setting up Appservice Discord (optional)

The playbook can install and configure [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) for you.

See the project's [documentation](https://github.com/Half-Shot/matrix-appservice-discord/blob/master/README.md) to learn what it does and why it might be useful to you.

Setup Instructions: 

loosely based on [this](https://github.com/Half-Shot/matrix-appservice-discord#setting-up)

1. Create a Discord Application [here](https://discordapp.com/developers/applications/me/create).
2. Retrieve Client ID and Bot token from this Application.
3. Enable the bridge with `matrix_appservice_discord_enabled: true` in your vars.yml and provide id and token.
4. Rerun playbook with "setup-all" tag. Restart with tag "start" afterwards.
5. Retrieve Discord invitelink from `{{ matrix_appservice_discord_base_path }}/invite_link` (this defaults to `/matrix/appservice-discord/invite_link`)
6. Invite the Bot to Discord servers you wish to bridge. Administrator permission is recommended.
7. Join the rooms by following this syntax `#_discord_guildid_channelid`
 - can be easily retrieved by logging into Discord in a browser and opening the desired channel. URL will have this format: discordapp.com/channels/guild_id/channel_id

Other configuration options are available via the `matrix_appservice_discord_configuration_extension_yaml` variable.