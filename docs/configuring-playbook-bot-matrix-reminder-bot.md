# Setting up matrix-reminder-bot (optional)

The playbook can install and configure [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) for you.

It's a bot you can use to **schedule one-off & recurring reminders and alarms**.

See the project's [documentation](https://github.com/anoadragon453/matrix-reminder-bot#usage) to learn what it does and why it might be useful to you.


## Registering the bot user

By default, the playbook will set up the bot with a username like this: `@bot.matrix-reminder-bot:DOMAIN`.

(to use a different username, adjust the `matrix_bot_matrix_reminder_bot_matrix_user_id_localpart` variable).

You **need to register the bot user manually** before setting up the bot. You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.matrix-reminder-bot password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_matrix_reminder_bot_enabled: true

# Adjust this to whatever password you chose when registering the bot user
matrix_bot_matrix_reminder_bot_matrix_user_password: PASSWORD_FOR_THE_BOT

# Adjust this to your timezone
matrix_bot_matrix_reminder_bot_reminders_timezone: Europe/London
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, start a chat with `@bot.matrix-reminder-bot:DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

You can also add the bot to any existing Matrix room (`/invite @bot.matrix-reminder-bot:DOMAIN`).

Basic usage is like this: `!remindme in 2 minutes; This is a test`

Send `!help reminders` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [Usage documentation](https://github.com/anoadragon453/matrix-reminder-bot#usage).
