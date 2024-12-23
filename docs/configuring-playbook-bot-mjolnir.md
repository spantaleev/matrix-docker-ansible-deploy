# Setting up Mjolnir (optional)

The playbook can install and configure the [Mjolnir](https://github.com/matrix-org/mjolnir) moderation bot for you.

See the project's [documentation](https://github.com/matrix-org/mjolnir/blob/main/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Register the bot account

The playbook does not automatically create users for you. You **need to register the bot user manually** before setting up the bot.

Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.mjolnir password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

If you would like Mjolnir to be able to deactivate users, move aliases, shutdown rooms, etc then it must be a server admin so you need to change `admin=no` to `admin=yes` in the command above.

### Obtain an access token

The bot requires an access token to be able to connect to your homeserver. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

⚠️ **Warning**: Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

### Make sure the account is free from rate limiting

If your homeserver's implementation is Synapse, you will need to prevent it from rate limiting the bot's account. **This is a required step. If you do not configure it, Mjolnir will crash.**

This can be done using Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users). They can be accessed both externally and internally.

To expose the APIs publicly, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file.

```yaml
matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true
```

The APIs can also be accessed via [Synapse Admin](https://github.com/etkecc/synapse-admin), a web UI tool you can use to administrate users, rooms, media, etc. on your Matrix server. The playbook can install and configure Synapse Admin for you. For details about it, see [this page](configuring-playbook-synapse-admin.md).

**Note**: access to the APIs is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, doing so is not recommended for additional security. See [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints).

To discharge rate limiting, run the following command on systems that ship curl (note that it does not work on outdated Windows 10). Even if the APIs are not exposed to the internet, you should still be able to run the command on the homeserver locally. Before running it, make sure to replace `@bot.mjolnir:example.com` with the MXID of your Mjolnir:

```sh
curl --header "Authorization: Bearer <access_token>" -X POST https://matrix.example.com/_synapse/admin/v1/users/@bot.mjolnir:example.com/override_ratelimit
```

You can obtain an access token for a homeserver admin account in the same way as you can do so for Mjolnir itself. If you have made Mjolnir an admin, you can just use the Mjolnir token.

### Create a management room

Using your own account, create a new invite only room that you will use to manage the bot. This is the room where you will see the status of the bot and where you will send commands to the bot, such as the command to ban a user from another room. Anyone in this room can control the bot so it is important that you only invite trusted users to this room.

If you make the management room encrypted (E2EE), then you MUST enable and use Pantalaimon (see [below](#configuration-with-e2ee-support)).

Once you have created the room you need to copy the room ID so you can tell the bot to use that room. In Element Web you can do this by going to the room's settings, clicking Advanced, and then copying the internal room ID. The room ID will look something like `!qporfwt:example.com`.

Finally invite the `@bot.mjolnir:example.com` account you created earlier into the room.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `MANAGEMENT_ROOM_ID_HERE`.

```yaml
# Enable Mjolnir
matrix_bot_mjolnir_enabled: true

matrix_bot_mjolnir_management_room: "MANAGEMENT_ROOM_ID_HERE"
```

### End-to-End Encryption support

Decide whether you want Mjolnir to be capable of operating in end-to-end encrypted (E2EE) rooms. This includes the management room and the moderated rooms.

To support E2EE, Mjolnir needs to [use Pantalaimon](configuring-playbook-pantalaimon.md).

#### Configuration with E2EE support

When using Pantalaimon, Mjolnir will log in to its bot account itself through Pantalaimon, so configure its username and password.

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
# Enable Pantalaimon. See docs/configuring-playbook-pantalaimon.md
matrix_pantalaimon_enabled: true

# Tell Mjolnir to use Pantalaimon
matrix_bot_mjolnir_pantalaimon_use: true

# User name and password for the bot you have created above. Required when using Pantalaimon.
matrix_bot_mjolnir_pantalaimon_username: "bot.mjolnir"
matrix_bot_mjolnir_pantalaimon_password: "PASSWORD_FOR_THE_BOT"
```

The playbook's `group_vars` will configure other required settings. If using this role separately without the playbook, you also need to configure the two URLs that Mjolnir uses to reach the homeserver, one through Pantalaimon and one "raw". This example is taken from the playbook's `group_vars`:

```yaml
# Endpoint URL that Mjolnir uses to interact with the Matrix homeserver (client-server API).
# Set this to the pantalaimon URL if you're using that.
matrix_bot_mjolnir_homeserver_url: "{{ 'http://matrix-pantalaimon:8009' if matrix_bot_mjolnir_pantalaimon_use else matrix_addons_homeserver_client_api_url }}"

# Endpoint URL that Mjolnir could use to fetch events related to reports (client-server API and /_synapse/),
# only set this to the public-internet homeserver client API URL, do NOT set this to the pantalaimon URL.
matrix_bot_mjolnir_raw_homeserver_url: "{{ matrix_addons_homeserver_client_api_url }}"
```

#### Configuration without E2EE support

When NOT using Pantalaimon, Mjolnir does not log in by itself and you must give it an access token for its bot account.

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `ACCESS_TOKEN_HERE` with the one created [above](#obtain-an-access-token).

```yaml
matrix_bot_mjolnir_access_token: "ACCESS_TOKEN_HERE"
```

### Adding Mjolnir synapse antispam module (optional)

To enable Mjolnir synapse antispam module, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_ext_spam_checker_mjolnir_antispam_enabled: true
matrix_synapse_ext_spam_checker_mjolnir_antispam_config_block_invites: true
matrix_synapse_ext_spam_checker_mjolnir_antispam_config_block_messages: false
matrix_synapse_ext_spam_checker_mjolnir_antispam_config_block_usernames: false
matrix_synapse_ext_spam_checker_mjolnir_antispam_config_ban_lists: []
```

### Extending the configuration

You can configure additional options by adding the `matrix_bot_mjolnir_configuration_extension_yaml` variable to your `inventory/host_vars/matrix.example.com/vars.yml` file.

For example, to change Mjolnir's `recordIgnoredInvites` option to `true`, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_mjolnir_configuration_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_bot_mjolnir_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_bot_mjolnir_configuration_yaml`.
  recordIgnoredInvites: true
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

- If you change the Pantalaimon's password (`matrix_bot_mjolnir_pantalaimon_password` in your `vars.yml` file) subsequently, its credentials on the homeserver won't be updated automatically. If you'd like to change the password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_mjolnir_pantalaimon_password` to let Pantalaimon know its new password.

## Usage

You can refer to the upstream [documentation](https://github.com/matrix-org/mjolnir) for additional ways to use and configure Mjolnir. Check out their [quickstart guide](https://github.com/matrix-org/mjolnir#quickstart-guide) for some basic commands you can give to the bot.
