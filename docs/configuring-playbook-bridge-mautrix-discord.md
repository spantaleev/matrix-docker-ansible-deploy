# Setting up Mautrix Discord (optional)

**Note**: bridging to [Discord](https://discordapp.com/) can also happen via the [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) and [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) bridges supported by the playbook.  
- For using as a Bot we recommend the [Appservice Discord](configuring-playbook-bridge-appservice-discord.md), because it supports plumbing.  
- For personal use with a discord account we recommend the `mautrix-discord` bridge (the one being discussed here), because it is the most fully-featured and stable of the 3 Discord bridges supported by the playbook.
The `mautrix-discord` bridge (the one being discussed here) is the most fully-featured and stable of the 3 Discord bridges supported by the playbook, so it's the one we recommend.

The playbook can install and configure [mautrix-discord](https://github.com/mautrix/discord) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/discord/index.html) to learn what it does and why it might be useful to you.


## Prerequisites

For using this bridge, you would **need to authenticate by scanning a QR code with the Discord app on your phone**.

You can delete the Discord app after the authentication process.

If this is a dealbreaker for you, consider using one of the other Discord bridges supported by the playbook: [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) or [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md). These come with their own complexity and limitations, however, so we recommend that you proceed with this one if possible.


## Installing

To enable the bridge, add this to your `vars.yml` file:

```yaml
matrix_mautrix_discord_enabled: true
```

You may optionally wish to add some [Additional configuration](#additional-configuration), or to [prepare for double-puppeting](#set-up-double-puppeting) before the initial installation.

After adjusting your `vars.yml` file, re-run the playbook and restart all services: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

To make use of the bridge, see [Usage](#usage) below.


### Additional configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/matrix-bridge-mautrix-discord/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/matrix-bridge-mautrix-discord/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_mautrix_discord_configuration_extension_yaml` variable


### Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

#### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

#### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Mautrix-Discord", "initial_device_display_name": "Mautrix-Discord"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Discord` device some time in the future, as that would break the Double Puppeting feature


## Usage

1. Start a chat with `@discordbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
2. Send a `login` command
3. You'll see a QR code which you need to scan with the Discord app on your phone. You can scan it with the camera app too, which will open Discord, which will then instruct you to scan it a 2nd time in the Discord app.
4. After confirming (in the Discord app) that you'd like to allow this login, the bot should respond with "Succcessfully authenticated as ..."
5. Now that you're logged in, you can send a `help` command to the bot again, to see additional commands you have access to
6. Some Direct Messages from Discord should start syncing automatically
7. If you'd like to bridge guilds:
- send `guilds status` to see the list of guilds
- for each guild that you'd like bridged, send `guilds bridge GUILD_ID --entire`
8. You may wish to uninstall the Discord app from your phone now. It's not needed for the bridge to function.
