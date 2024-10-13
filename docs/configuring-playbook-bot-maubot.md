# Setting up maubot (optional)

The playbook can install and configure [maubot](https://github.com/maubot/maubot) for you.

After setting up maubot, you can use the web management interface to make it do things.
The default location of the management interface is `matrix.<your-domain>/_matrix/maubot/`

See the project's [documentation](https://docs.mau.fi/maubot/usage/basic.html) to learn what it
does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_maubot_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_maubot_login: bot.maubot

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_maubot_initial_password: PASSWORD_FOR_THE_BOT

matrix_bot_maubot_admins:
  - yourusername: securepassword
```

You can add multiple admins. The admin accounts are only used to access the maubot administration interface.


## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all`

**Notes**:

- if you change the bot password (`matrix_bot_maubot_initial_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_maubot_initial_password` to let the bot know its new password

## Usage

You can visit `matrix.<your-domain>/_matrix/maubot/` to manage your available plugins, clients and instances.

You should start in the following order
1. **Create one or more clients:** A client is a matrix account which the bot will use to message. By default, the playbook creates a `bot.maubot` account (as per the configuration above). You only need to [obtain an access token](#obtaining-an-access-token) for it
2. **Upload some Plugins:** Plugins can be obtained from [here](https://github.com/maubot/maubot#plugins) or any other source.
3. **Create an instance:** An instance is the actual bot. You have to specify a client which the bot instance will use
and the plugin (how the bot will behave)

## Obtaining an access token

This can be done via `mbc login` then `mbc auth` (see the [maubot documentation](https://docs.mau.fi/maubot/usage/cli/auth.html)). To run these commands, you'll first need to `exec` into the maubot container with `docker exec -it matrix-bot-maubot sh`.

Alternatively, you can follow our generic [obtain an access token](obtaining-access-tokens.md) documentation. Be aware that you'd better use the **Obtain an access token via curl** method (not **Obtain an access token via Element**) as the latter will give your bot issues in encrypted rooms. Read [more](https://docs.mau.fi/maubot/usage/basic.html#creating-clients).
