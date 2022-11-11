# Setting up matrix-registration-bot (optional)

The playbook can install and configure [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) for you.

The bot allows you to easily **create and manage registration tokens**. It can be used for an invitation-based server,
where you invite someone by sending them a registration token. They can register as normal but have to provide a valid
registration token in a final step  of the registration.

See the project's [documentation](https://github.com/moan0s/matrix-registration-bot#supported-commands) to learn what it
does and why it might be useful to you.


## Registering the bot user

By default, the playbook will set use the bot with a username like this: `@bot.matrix-registration-bot:DOMAIN`.

(to use a different username, adjust the `matrix_bot_matrix_registration_bot_matrix_user_id_localpart` variable).

For [other bots supported by the playbook](configuring-playbook.md#bots), Matrix bot user accounts are created and put to use automatically. For `matrix-registration-bot`, however, this is not the case - you **need to register the bot user manually** before setting up the bot. You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.matrix-registration-bot password=PASSWORD_FOR_THE_BOT admin=yes' --tags=register-user
```

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

## Obtaining an admin access token

In order to use the bot you need to add an admin user's access token token to the configuration. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_matrix_registration_bot_enabled: true
# Token obtained via logging into the bot account (see above)
matrix_bot_matrix_registration_bot_bot_access_token: "syt_bW9hbm9z_XXXXXXXXXXXXXr_2kuzbE"

# Enables registration
matrix_synapse_enable_registration: true

# Restrict registration to users with a token
matrix_synapse_registration_requires_token: true
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, create a **non-encrypted** room and invite `@bot.matrix-registration-bot:DOMAIN` (where `DOMAIN` is your base domain, not the `matrix.` domain).

In this room send `help` and the bot will reply with all options.

You can also refer to the upstream [Usage documentation](https://github.com/moan0s/matrix-registration-bot#supported-commands).
If you have any questions, or if you need help setting it up, read the [troublshooting guide](https://github.com/moan0s/matrix-registration-bot/blob/main/docs/troubleshooting.md)
or join [#matrix-registration-bot:hyteck.de](https://matrix.to/#/#matrix-registration-bot:hyteck.de).
