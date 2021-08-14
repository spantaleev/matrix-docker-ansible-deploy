# Setting up Mautrix Signal (optional)

The playbook can install and configure [mautrix-signal](https://github.com/tulir/mautrix-signal) for you.

See the project's [documentation](https://github.com/tulir/mautrix-signal/wiki) to learn what it does and why it might be useful to you.

**Note/Prerequisite**: If you're running with the Postgres database server integrated by the playbook (which is the default), you don't need to do anything special and can easily proceed with installing. However, if you're [using an external Postgres server](configuring-playbook-external-postgres.md), you'd need to manually prepare a Postgres database for this bridge and adjust the variables related to that (`matrix_mautrix_signal_database_*`).

Use the following playbook configuration:

```yaml
matrix_mautrix_signal_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue.

The relay bot functionality is off by default. If you would like to enable the relay bot, add the following to your `vars.yml` file:
```yaml
matrix_mautrix_signal_relaybot_enabled: true
```
If you want to activate the relay bot in a room, use `!signal set-relay`.
Use `!signal unset-relay` to deactivate.
Additionally the permissions for the bridge grant user rights to all base domain users in case the relay bot is disabled, or relay rights in case the relay bot is enabled.

If you would like to have a more specific setting of the permissions you can set the permissions as follows (example). For more details see also [mautrix-bridge documentation](https://docs.mau.fi/bridges/python/signal/relay-mode.html)
```yaml
matrix_mautrix_signal_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:YOUR_DOMAIN': admin
      YOUR_DOMAIN: user
      '*': relay
```

You may wish to look at `roles/matrix-bridge-mautrix-signal/templates/config.yaml.j2` to find more information on the permissions settings and other options you would like to configure.

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://github.com/tulir/mautrix-signal/wiki/Authentication#double-puppeting) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Mautrix-Signal", "initial_device_display_name": "Mautrix-Signal"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Signal` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@signalbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
