# Setting up MX Puppet GroupMe bridging (optional)

The playbook can install and configure [mx-puppet-groupme](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme) for you.

See the project page to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [GroupMe](https://groupme.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_groupme_enabled: true
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

Once the bot is enabled you need to start a chat with `GroupMe Puppet Bridge` with the handle `@_groupmepuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

One authentication method is available.

To link your GroupMe account, go to [dev.groupme.com](https://dev.groupme.com/), sign in, and select "Access Token" from the top menu. Copy the token and message the bridge with:

```
link <access token>
```

Once logged in, send `listrooms` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Also send `help` to the bot to see the commands available.
