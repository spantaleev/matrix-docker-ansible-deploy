# Setting up Mautrix Telegram (optional)

The playbook can install and configure [mautrix-telegram](https://github.com/mautrix/telegram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/telegram/index.html) to learn what it does and why it might be useful to you.

You'll need to obtain API keys from [https://my.telegram.org/apps](https://my.telegram.org/apps) and then use the following playbook configuration:

```yaml
matrix_mautrix_telegram_enabled: true
matrix_mautrix_telegram_api_id: YOUR_TELEGRAM_APP_ID
matrix_mautrix_telegram_api_hash: YOUR_TELEGRAM_API_HASH
```

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging.

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Mautrix-Telegram", "initial_device_display_name": "Mautrix-Telegram"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send `login-matrix` to the bot and follow instructions about how to send the access token to it

- make sure you don't log out the `Mautrix-Telegram` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@telegrambot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

If you want to use the relay-bot feature ([relay bot documentation](https://docs.mau.fi/bridges/python/telegram/relay-bot.html)), which allows anonymous user to chat with telegram users, use the following additional playbook configuration:

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
      '@user:DOMAIN': admin
```

More details about permissions in this example:
https://github.com/mautrix/telegram/blob/master/mautrix_telegram/example-config.yaml#L410
