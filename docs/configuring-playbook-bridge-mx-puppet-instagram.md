# Setting up MX Puppet Instagram bridging (optional)

The playbook can install and configure [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) for you.

This allows you to bridge Instagram DirectMessages into Matrix.

## Adjusting the playbook configuration

To enable the [Instagram](https://www.instagram.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_instagram_enabled: true
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with `just` program are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)

## Usage

Once the bot is enabled, you need to start a chat with `Instagram Puppet Bridge` with the handle `@_instagrampuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `link <username> <password>` to the bridge bot to link your instagram account.

The `list` commands shows which accounts are linked and which `puppetId` is associated.

For double-puppeting, you probably want to issue these commands:

- `settype $puppetId puppet` to enable puppeting for the link (instead of relaying)
- `setautoinvite $puppetId 1` to automatically invite you to chats
- `setmatrixtoken $accessToken` to set the access token to enable puppeting from the other side (the "double" in double puppeting)

If you are linking only one Instagram account, your `$puppetId` is probably 1, but use the `list` command find out.

The `help` command shows which commands are available, though at the time of writing, not every command is fully implemented.
