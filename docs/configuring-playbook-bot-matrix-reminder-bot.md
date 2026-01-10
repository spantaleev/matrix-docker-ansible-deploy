<!--
SPDX-FileCopyrightText: 2020 - 2022 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up matrix-reminder-bot (optional)

The playbook can install and configure [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) for you.

It's a bot you can use to **schedule one-off & recurring reminders and alarms**.

See the project's [documentation](https://github.com/anoadragon453/matrix-reminder-bot/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_matrix_reminder_bot_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_matrix_reminder_bot_matrix_user_id_localpart: bot.matrix-reminder-bot

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_bot_matrix_reminder_bot_matrix_user_password: PASSWORD_FOR_THE_BOT

# Adjust this to your timezone
matrix_bot_matrix_reminder_bot_reminders_timezone: Europe/London
```

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-matrix-reminder-bot/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bot-matrix-reminder-bot/templates/config.yaml.j2` for the bot's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_bot_matrix_reminder_bot_configuration_extension_yaml` variable

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

- If you change the bot password (`matrix_bot_matrix_reminder_bot_matrix_user_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_matrix_reminder_bot_matrix_user_password` to let the bot know its new password.

## Usage

To use the bot, start a chat with `@bot.matrix-reminder-bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You can also add the bot to any existing Matrix room (`/invite @bot.matrix-reminder-bot:example.com`).

Basic usage is like this: `!remindme in 2 minutes; This is a test`

Send `!help reminders` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [Usage documentation](https://github.com/anoadragon453/matrix-reminder-bot#usage).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bot-matrix-reminder-bot`.

### Increase logging verbosity

The default logging level for this component is `INFO`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_bot_matrix_reminder_bot_configuration_extension_yaml: |
  logging:
    # Valid values: ERROR, WARNING, INFO, DEBUG
    level: DEBUG
```
