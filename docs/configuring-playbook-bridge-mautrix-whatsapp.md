# Setting up Mautrix Whatsapp (optional)

The playbook can install and configure [mautrix-whatsapp](https://github.com/mautrix/whatsapp) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/whatsapp/index.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_whatsapp_enabled: true
```

Whatsapp multidevice beta is required, now it is enough if Whatsapp is connected to the Internet every 2 weeks.

The relay bot functionality is off by default. If you would like to enable the relay bot, add the following to your `vars.yml` file:
```yaml
matrix_mautrix_whatsapp_bridge_relay_enabled: true
```

By default, only admins are allowed to set themselves as relay users. To allow anyone on your homeserver to set themselves as relay users add this to your `vars.yml` file:
```yaml
matrix_mautrix_whatsapp_bridge_relay_admin_only: false
```

If you want to activate the relay bot in a room, use `!wa set-relay`.
Use `!wa unset-relay` to deactivate.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Appservice Double Puppet or Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service or the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

Enabling double puppeting by enabling the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service works at the time of writing, but is deprecated and will stop working in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Whatsapp` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@whatsappbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).
