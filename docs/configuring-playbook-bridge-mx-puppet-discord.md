# Setting up MX Puppet Discord bridging (optional)

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md)and [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridges supported by the playbook.   
- For using as a Bot we recommend the [Appservice Discord](configuring-playbook-bridge-appservice-discord.md), because it supports plumbing.  
- For personal use with a discord account we recommend the [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) bridge, because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.

The playbook can install and configure [mx-puppet-discord](https://gitlab.com/mx-puppet/discord/mx-puppet-discord) for you.

See the project page to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [Discord](https://discordapp.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_discord_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once the bot is enabled you need to start a chat with `Discord Puppet Bridge` with the handle `@_discordpuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token. See mx-puppet-discord [documentation](https://gitlab.com/mx-puppet/discord/mx-puppet-discord) for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Also send `help` to the bot to see the commands available.
