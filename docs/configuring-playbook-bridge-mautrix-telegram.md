# Setting up Mautrix Telegram bridging (optional)

The playbook can install and configure [mautrix-telegram](https://github.com/mautrix/telegram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/telegram/index.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

You'll need to obtain API keys from [https://my.telegram.org/apps](https://my.telegram.org/apps) and then add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_telegram_enabled: true
matrix_mautrix_telegram_api_id: YOUR_TELEGRAM_APP_ID
matrix_mautrix_telegram_api_hash: YOUR_TELEGRAM_API_HASH
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Appservice Double Puppet or Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service or the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

Enabling double puppeting by enabling the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service works at the time of writing, but is deprecated and will stop working in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging.

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send `login-matrix` to the bot and follow instructions about how to send the access token to it

- make sure you don't log out the `Mautrix-Telegram` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@telegrambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

If you want to use the relay-bot feature ([relay bot documentation](https://docs.mau.fi/bridges/python/telegram/relay-bot.html)), which allows anonymous user to chat with telegram users, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_telegram_bot_token: YOUR_TELEGRAM_BOT_TOKEN
matrix_mautrix_telegram_configuration_extension_yaml: |
  bridge:
    permissions:
      '*': relaybot
```

You might also want to give permissions to administrate the bot:
```yaml
matrix_mautrix_telegram_configuration_extension_yaml: |
  bridge:
    permissions:
      '@user:example.com': admin
```

More details about permissions in this example: https://github.com/mautrix/telegram/blob/master/mautrix_telegram/example-config.yaml#L410

If you like to exclude all groups from syncing and use the Telgeram-Bridge only for direct chats, you can add the following additional playbook configuration:
```yaml
matrix_mautrix_telegram_filter_mode: whitelist
```
