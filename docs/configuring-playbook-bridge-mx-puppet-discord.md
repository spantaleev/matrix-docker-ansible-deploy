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

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

Once the bot is enabled you need to start a chat with `Discord Puppet Bridge` with the handle `@_discordpuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token. See mx-puppet-discord [documentation](https://gitlab.com/mx-puppet/discord/mx-puppet-discord) for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Also send `help` to the bot to see the commands available.
