# Setting up Mautrix Signal (optional)

The playbook can install and configure [mautrix-signal](https://github.com/mautrix/signal) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/signal/index.html) to learn what it does and why it might be useful to you.

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
By default, any user on your homeserver will be able to use the bridge.
If you enable the relay bot functionality, it will relay every user's messages in a portal room - no matter which homeserver they're from.

Different levels of permission can be granted to users:

* relay - Allowed to be relayed through the bridge, no access to commands;
* user - Use the bridge with puppeting;
* admin - Use and administer the bridge.

The permissions are following the sequence: nothing < relay < user < admin.

The default permissions are set as follows:
```yaml
permissions:
  '*': relay
  YOUR_DOMAIN: user
```

If you want to augment the preset permissions, you might want to set the additional permissions with the following settings in your `vars.yml` file:
```yaml
matrix_mautrix_signal_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:YOUR_DOMAIN': admin
```

This will add the admin permission to the specific user, while keepting the default permissions.

In case you want to replace the default permissions settings **completely**, populate the following item within your `vars.yml` file:
```yaml
matrix_mautrix_signal_bridge_permissions: |
  '@ADMIN:YOUR_DOMAIN': admin
  '@USER:YOUR_DOMAIN' : user
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-signal/templates/config.yaml.j2` to find more information on the permissions settings and other options you would like to configure.

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Signal` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@signalbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
