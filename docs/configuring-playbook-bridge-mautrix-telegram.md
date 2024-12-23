# Setting up Mautrix Telegram bridging (optional)

The playbook can install and configure [mautrix-telegram](https://github.com/mautrix/telegram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/telegram/index.html) to learn what it does and why it might be useful to you.

## Prerequisite (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

For details about configuring Double Puppeting for this bridge, see the section below: [Set up Double Puppeting](#-set-up-double-puppeting)

## Adjusting the playbook configuration

You'll need to obtain API keys from [https://my.telegram.org/apps](https://my.telegram.org/apps) and then add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_telegram_enabled: true
matrix_mautrix_telegram_api_id: YOUR_TELEGRAM_APP_ID
matrix_mautrix_telegram_api_hash: YOUR_TELEGRAM_API_HASH
```

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

To use the bridge, you need to start a chat with `@telegrambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

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
      '@alice:{{ matrix_domain }}': admin
```

More details about permissions in this example: https://github.com/mautrix/telegram/blob/master/mautrix_telegram/example-config.yaml#L410

If you like to exclude all groups from syncing and use the Telgeram-Bridge only for direct chats, you can add the following additional playbook configuration:

```yaml
matrix_mautrix_telegram_filter_mode: whitelist
```

### 💡 Set up Double Puppeting

After successfully enabling bridging, you may wish to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do).

To set it up, you have 2 ways of going about it.

#### Method 1: automatically, by enabling Appservice Double Puppet or Shared Secret Auth

The bridge automatically performs Double Puppeting if [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service is configured and enabled on the server for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

Enabling double puppeting by enabling the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service works at the time of writing, but is deprecated and will stop working in the future.

#### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging.

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to obtain one](obtaining-access-tokens.md).

- send `login-matrix` to the bot and follow instructions about how to send the access token to it

- make sure you don't log out the `Mautrix-Telegram` device some time in the future, as that would break the Double Puppeting feature
