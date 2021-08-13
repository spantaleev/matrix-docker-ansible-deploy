# Setting up MX Puppet Steam (optional)

The playbook can install and configure
[mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Steam](https://steampowered.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_steam_enabled: true
```


## Usage

Once the bot is enabled you need to start a chat with `Steam Puppet Bridge` with
the handle `@_steampuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token.
See mx-puppet-steam [documentation](https://github.com/icewind1991/mx-puppet-steam)
for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
