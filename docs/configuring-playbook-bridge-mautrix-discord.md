# Setting up Mautrix Discord bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) and [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) bridges supported by the playbook.
- For using as a Bot we recommend the [Appservice Discord](configuring-playbook-bridge-appservice-discord.md), because it supports plumbing.
- For personal use with a discord account we recommend the `mautrix-discord` bridge (the one being discussed here), because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.

The playbook can install and configure [mautrix-discord](https://github.com/mautrix/discord) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/discord/index.html) to learn what it does and why it might be useful to you.

## Prerequisites

There are 2 ways to login to discord using this bridge, either by [scanning a QR code](#method-1-login-using-qr-code-recommended) using the Discord mobile app **or** by using a [Discord token](#method-2-login-using-discord-token-not-recommended).

If this is a dealbreaker for you, consider using one of the other Discord bridges supported by the playbook: [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) or [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md). These come with their own complexity and limitations, however, so we recommend that you proceed with this one if possible.

### Enable Appservice Double Puppet or Shared Secret Auth (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_discord_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: common relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#setting-the-bot-s-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

### Logging in

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/go/discord/authentication.html).

#### Method 1: Login using QR code (recommended)

For using this bridge, you would need to authenticate by **scanning a QR code** with the Discord app on your phone.

You can delete the Discord app after the authentication process.

#### Method 2: Login using Discord token (not recommended)

To acquire the token, open Discord in a private browser window. Then open the developer settings (keyboard shortcut might be "ctrl+shift+i" or by pressing "F12"). Navigate to the "Network" tab then reload the page. In the URL filter or search bar type "/api" and find the response with the file name of "library". Under the request headers you should find a variable called "Authorization", this is the token to your Discord account. After copying the token, you can close the browser window.

### Bridging

1. Start a chat with `@discordbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).
2. If you would like to login to Discord using a token, send `login-token` command, otherwise, send `login-qr` command.
3. You'll see a QR code which you need to scan with the Discord app on your phone. You can scan it with the camera app too, which will open Discord, which will then instruct you to scan it a 2nd time in the Discord app.
4. After confirming (in the Discord app) that you'd like to allow this login, the bot should respond with "Succcessfully authenticated as …"
5. Now that you're logged in, you can send `help` to the bot to see the available commands.
6. Some Direct Messages from Discord should start syncing automatically
7. If you'd like to bridge guilds:
    - send `guilds status` to see the list of guilds
    - for each guild that you'd like bridged, send `guilds bridge GUILD_ID --entire`
8. You may wish to uninstall the Discord app from your phone now. It's not needed for the bridge to function.

### Relaying

The bridge supports using Discord's webhook feature to relay messages from Matrix users who haven't logged into the bridge. See [the official documentation](https://docs.mau.fi/bridges/go/discord/relay.html#setup) for setting up webhook relaying.
