# Setting up matrix-registration-bot (optional)

The playbook can install and configure [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) for you.

The bot allows you to easily **create and manage registration tokens** aka. invitation codes. It can be used for an invitation-based server, where you invite someone by sending them a registration token (tokens look like this: `rbalQ0zkaDSRQCOp`). They can register as per normal but have to provide a valid registration token in the final step of the registration process.

See the project's [documentation](https://github.com/moan0s/matrix-registration-bot/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_matrix_registration_bot_enabled: true

# By default, the playbook will set use the bot with a username like this: `@bot.matrix-registration-bot:example.com`.
# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_matrix_registration_bot_matrix_user_id_localpart: bot.matrix-registration-bot

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_bot_matrix_registration_bot_bot_password: PASSWORD_FOR_THE_BOT

# Enables registration
matrix_synapse_enable_registration: true

# Restrict registration to users with a token
matrix_synapse_registration_requires_token: true
```

The bot account will be created automatically.

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

- If you change the bot password (`matrix_bot_matrix_registration_bot_bot_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_matrix_registration_bot_bot_password` to let the bot know its new password.

## Usage

To use the bot, start a chat with `@bot.matrix-registration-bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `help` to the bot to see the available commands.

You can also refer to the upstream [Usage documentation](https://github.com/moan0s/matrix-registration-bot#supported-commands).

If you have any questions, or if you need help setting it up, read the [troublshooting guide](https://github.com/moan0s/matrix-registration-bot/blob/main/docs/troubleshooting.md) or join [#matrix-registration-bot:hyteck.de](https://matrix.to/#/#matrix-registration-bot:hyteck.de).

To clean the cache (session & encryption data) after you changed the bot's username, changed the login method from access_token to password etc… you can use:

```sh
just run-tags bot-matrix-registration-bot-clean-cache
```
