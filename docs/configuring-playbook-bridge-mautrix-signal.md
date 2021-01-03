# Setting up Mautrix Signal (optional)

The playbook can install and configure [mautrix-signal](https://github.com/tulir/mautrix-signal) for you.

See the project's [documentation](https://github.com/tulir/mautrix-signal/wiki) to learn what it does and why it might be useful to you.

**Note/Prerequisite**: If you're running with the Postgres database server integrated by the playbook (which is the default), you don't need to do anything special and can easily proceed with installing. However, if you're [using an external Postgres server](configuring-playbook-external-postgres.md), you'd need to manually prepare a Postgres database for this bridge and adjust the variables related to that (`matrix_mautrix_signal_database_*`).

Use the following playbook configuration:

```yaml
matrix_mautrix_signal_enabled: true
```

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://github.com/tulir/mautrix-whatsapp/wiki/Authentication#replacing-whatsapp-accounts-matrix-puppet-with-matrix-account) (hint: you most likely do), you have 2 ways of going about it.

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
