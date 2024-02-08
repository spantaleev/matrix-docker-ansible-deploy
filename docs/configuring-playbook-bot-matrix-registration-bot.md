# Setting up matrix-registration-bot (optional)

The playbook can install and configure [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) for you.

The bot allows you to easily **create and manage registration tokens** aka. invitation codes.
It can be used for an invitation-based server, where you invite someone by sending them a registration token (tokens look like this: `rbalQ0zkaDSRQCOp`). They can register as per normal but have to provide a valid registration token in the final step of the registration process.

See the project's [documentation](https://github.com/moan0s/matrix-registration-bot#supported-commands) to learn what it
does and why it might be useful to you.


## Configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_matrix_registration_bot_enabled: true

# By default, the playbook will set use the bot with a username like this: `@bot.matrix-registration-bot:DOMAIN`.
# To use a different username, uncomment & adjust the variable below:
# matrix_bot_matrix_registration_bot_matrix_user_id_localpart: bot.matrix-registration-bot

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_matrix_registration_bot_bot_password: PASSWORD_FOR_THE_BOT

# Enables registration
matrix_synapse_enable_registration: true

# Restrict registration to users with a token
matrix_synapse_registration_requires_token: true
```

The bot account will be created automatically.

## Installing

After configuring the playbook, re-run the [installation](installing.md) command again: `just install-all` or `just setup-all`

## Usage

To use the bot, message `@bot.matrix-registration-bot:DOMAIN` (where `DOMAIN` is your base domain, not the `matrix.` domain).

In this room send `help` and the bot will reply with all options.

You can also refer to the upstream [Usage documentation](https://github.com/moan0s/matrix-registration-bot#supported-commands).
If you have any questions, or if you need help setting it up, read the [troublshooting guide](https://github.com/moan0s/matrix-registration-bot/blob/main/docs/troubleshooting.md)
or join [#matrix-registration-bot:hyteck.de](https://matrix.to/#/#matrix-registration-bot:hyteck.de).

To clean the cache (session&encryption data) after you changed the bot's username, changed the login methon form access_token to password etc.. you can use

```bash
just run-tags bot-matrix-registration-bot-clean-cache
```
