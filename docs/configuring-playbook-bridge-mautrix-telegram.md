<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 Hugues Morisset
SPDX-FileCopyrightText: 2019 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2021 Panagiotis Georgiadis
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Iikka Järvenpää
SPDX-FileCopyrightText: 2022 Marko Weltzer
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Telegram bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-telegram](https://github.com/mautrix/telegram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/telegram/index.html) to learn what it does and why it might be useful to you.

## Prerequisites

### Obtain a Telegram API key

To use the bridge, you'd need to obtain an API key from [https://my.telegram.org/apps](https://my.telegram.org/apps).

### Enable Appservice Double Puppet or Shared Secret Auth (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Notes**:

- Double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

- If you decided to enable Double Puppeting manually, send `login-matrix` to the bot in order to receive an instruction about how to send an access token to it.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `YOUR_TELEGRAM_APP_ID` and `YOUR_TELEGRAM_API_HASH`.

```yaml
matrix_mautrix_telegram_enabled: true
matrix_mautrix_telegram_api_id: YOUR_TELEGRAM_APP_ID
matrix_mautrix_telegram_api_hash: YOUR_TELEGRAM_API_HASH
```

### Relaying

### Enable relay-bot (optional)

If you want to use the relay-bot feature ([relay bot documentation](https://docs.mau.fi/bridges/python/telegram/relay-bot.html)), which allows anonymous user to chat with telegram users, add the following configuration to your `vars.yml` file:

```yaml
matrix_mautrix_telegram_bot_token: YOUR_TELEGRAM_BOT_TOKEN
matrix_mautrix_telegram_configuration_extension_yaml: |
  bridge:
    permissions:
      '*': relaybot
```

### Configure a user as an administrator of the bridge (optional)

You might also want to give permissions to a user to administrate the bot. See [this section](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional) on the common guide for details about it.

More details about permissions in this example: https://github.com/mautrix/telegram/blob/master/mautrix_telegram/example-config.yaml#L410

### Use the bridge for direct chats only (optional)

If you want to exclude all groups from syncing and use the Telegram-Bridge only for direct chats, add the following configuration to your `vars.yml` file:

```yaml
matrix_mautrix_telegram_filter_mode: whitelist
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: common relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@telegrambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You can then follow instructions on the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/telegram/authentication.html).

After logging in, the bridge will create portal rooms for all of your Telegram groups and invite you to them. Note that the bridge won't automatically create rooms for private chats.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-telegram`.

### Increase logging verbosity

The default logging level for this component is `WARNING`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_mautrix_telegram_logging_level: DEBUG
```
