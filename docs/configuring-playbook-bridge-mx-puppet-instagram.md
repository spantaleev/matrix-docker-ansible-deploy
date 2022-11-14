# Setting up mx-puppet-instagram (optional)

The playbook can install and configure
[mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) for you.

This allows you to bridge Instagram DirectMessages into Matrix.

To enable the [Instagram](https://www.instagram.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_instagram_enabled: true
```


## Usage

Once the bot is enabled, you need to start a chat with `Instagram Puppet Bridge` with
the handle `@_instagrampuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Send `link <username> <password>` to the bridge bot to link your instagram account.

The `list` commands shows which accounts are linked and which `puppetId` is associated.

For double-puppeting, you probably want to issue these commands:

- `settype $puppetId puppet` to enable puppeting for the link (instead of relaying)
- `setautoinvite $puppetId 1` to automatically invite you to chats
- `setmatrixtoken $accessToken` to set the access token to enable puppeting from the other side (the "double" in double puppeting)

If you are linking only one Instagram account, your `$puppetId` is probably 1, but use the `list` command find out.

The `help` command shows which commands are available, though at the time of writing, not every command is fully implemented.

