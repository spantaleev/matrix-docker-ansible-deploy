# Setting up MX Puppet Discord (optional)

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) bridge supported by the playbook.

The playbook can install and configure
[mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Discord](https://discordapp.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_discord_enabled: true
matrix_mx_puppet_discord_client_id: ""
matrix_mx_puppet_discord_client_secret: ""
```


## Usage

Once the bot is enabled you need to start a chat with `Discord Puppet Bridge` with
the handle `@_discordpuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token.
See mx-puppet-discord [documentation](https://github.com/matrix-discord/mx-puppet-discord)
for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
