# Setting up MX Puppet Skype (optional)

The playbook can install and configure
[mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Skype](https://www.skype.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_skype_enabled: true
```


## Usage

Once the bot is enabled you need to start a chat with `Skype Puppet Bridge` with
the handle `@_skypepuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Send `link <username> <password>` to the bridge bot to link your skype account.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
