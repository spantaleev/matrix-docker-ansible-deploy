# Setting up MX Puppet GroupMe (optional)

The playbook can install and configure [mx-puppet-groupme](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme) for you.

See the project page to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [GroupMe](https://groupme.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_groupme_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once the bot is enabled you need to start a chat with `GroupMe Puppet Bridge` with the handle `@_groupmepuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

One authentication method is available.

To link your GroupMe account, go to [dev.groupme.com](https://dev.groupme.com/), sign in, and select "Access Token" from the top menu. Copy the token and message the bridge with:

```
link <access token>
```

Once logged in, send `listrooms` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Also send `help` to the bot to see the commands available.
