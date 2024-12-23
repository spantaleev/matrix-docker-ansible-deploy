# Setting up maubot (optional)

The playbook can install and configure [maubot](https://github.com/maubot/maubot) for you.

After setting up maubot, you can use the web management interface to make it do things. The default location of the management interface is `matrix.example.com/_matrix/maubot/`

See the project's [documentation](https://docs.mau.fi/maubot/usage/basic.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_maubot_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_maubot_login: bot.maubot

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_bot_maubot_initial_password: PASSWORD_FOR_THE_BOT

matrix_bot_maubot_admins:
  - yourusername: securepassword
```

You can add multiple admins. The admin accounts are only used to access the maubot administration interface.

### Adjusting the maubot URL

By default, this playbook installs maubot on the `matrix.` subdomain, at the `/_matrix/maubot/` path (https://matrix.example.com/_matrix/maubot/). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_bot_maubot_hostname` and `matrix_bot_maubot_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_bot_maubot_hostname: maubot.example.com
matrix_bot_maubot_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the maubot domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

- If you change the bot password (`matrix_bot_maubot_initial_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_maubot_initial_password` to let the bot know its new password.

## Usage

By default, you can visit `matrix.example.com/_matrix/maubot/` to manage your available plugins, clients and instances.

You should start in the following order
1. **Create one or more clients**: A client is a Matrix account which the bot will use to message. By default, the playbook creates a `bot.maubot` account (as per the configuration above). You only need to [obtain an access token](#obtaining-an-access-token) for it
2. **Upload some Plugins**: Plugins can be obtained from [here](https://github.com/maubot/maubot#plugins) or any other source.
3. **Create an instance**: An instance is the actual bot. You have to specify a client which the bot instance will use and the plugin (how the bot will behave)

## Obtain an access token

This can be done via `mbc login` then `mbc auth` (see the [maubot documentation](https://docs.mau.fi/maubot/usage/cli/auth.html)). To run these commands, you'll first need to `exec` into the maubot container with `docker exec -it matrix-bot-maubot sh`.

Alternatively, you can refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md). Be aware that you'd better use the **Obtain an access token via curl** method (not **Obtain an access token via Element Web**) as the latter will causes issues to your bot in encrypted rooms. Read [more](https://docs.mau.fi/maubot/usage/basic.html#creating-clients).

⚠️ **Warning**: Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.
