# Setting up matrix-reminder-bot (optional)

The playbook can install and configure [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) for you.

It's a bot you can use to **schedule one-off & recurring reminders and alarms**.

See the project's [documentation](https://github.com/anoadragon453/matrix-reminder-bot#usage) to learn what it does and why it might be useful to you.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_matrix_reminder_bot_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_matrix_reminder_bot_matrix_user_id_localpart: bot.matrix-reminder-bot

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_matrix_reminder_bot_matrix_user_password: PASSWORD_FOR_THE_BOT

# Adjust this to your timezone
matrix_bot_matrix_reminder_bot_reminders_timezone: Europe/London
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- the `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account

- if you change the bot password (`matrix_bot_matrix_reminder_bot_matrix_user_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_matrix_reminder_bot_matrix_user_password` to let the bot know its new password


## Usage

To use the bot, start a chat with `@bot.matrix-reminder-bot:DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

You can also add the bot to any existing Matrix room (`/invite @bot.matrix-reminder-bot:DOMAIN`).

Basic usage is like this: `!remindme in 2 minutes; This is a test`

Send `!help reminders` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [Usage documentation](https://github.com/anoadragon453/matrix-reminder-bot#usage).
