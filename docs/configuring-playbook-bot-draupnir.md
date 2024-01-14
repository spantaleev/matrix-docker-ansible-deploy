# Setting up draupnir (optional)

The playbook can install and configure the [draupnir](https://github.com/the-draupnir-project/Draupnir) moderation bot for you.

See the project's [documentation](https://github.com/the-draupnir-project/Draupnir) to learn what it does and why it might be useful to you.

If your migrating from Mjolnir skip to step 5b.

## 1. Register the bot account

The playbook does not automatically create users for you. The bot requires an access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.draupnir password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

If you would like draupnir to be able to deactivate users, move aliases, shutdown rooms, show abuse reports ([see below](#abuse-reports)), etc then it must be a server admin so you need to change `admin=no` to `admin=yes` in the command above.


## 2. Get an access token

Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).


## 3. Make sure the account is free from rate limiting

You will need to prevent Synapse from rate limiting the bot's account. This is not an optional step. If you do not do this step draupnir will crash. This can be done using Synapse's [admin API](https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users). Please ask for help if you are uncomfortable with these steps or run into issues.

If your Synapse Admin API is exposed to the internet for some reason like running the Synapse Admin Role [Link](/docs/configuring-playbook-synapse-admin.md) or running `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true` in your playbook config. If your API is not externally exposed you should still be able to on the local host for your synapse run these commands.

The following command works on semi up to date Windows 10 installs and All Windows 11 installations and other systems that ship curl. `curl --header "Authorization: Bearer <access_token>" -X POST https://matrix.example.com/_synapse/admin/v1/users/@example:example.com/override_ratelimit` Replace `@example:example.com` with the MXID of your Draupnir and example.com with your homeserver domain. You can easily obtain an access token for a homeserver admin account the same way you can obtain an access token for Draupnir it self. If you made Draupnir Admin you can just use the Draupnir token.



## 4. Create a management room

Using your own account, create a new invite only room that you will use to manage the bot. This is the room where you will see the status of the bot and where you will send commands to the bot, such as the command to ban a user from another room. Anyone in this room can control the bot so it is important that you only invite trusted users to this room. The room must be unencrypted since the playbook does not support installing Pantalaimon yet.

Once you have created the room you need to copy the room ID so you can tell the bot to use that room. In Element you can do this by going to the room's settings, clicking Advanced, and then coping the internal room ID. The room ID will look something like `!QvgVuKq0ha8glOLGMG:DOMAIN`.

Finally invite the `@bot.draupnir:DOMAIN` account you created earlier into the room.


## 5a. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

You must replace `ACCESS_TOKEN_FROM_STEP_2_GOES_HERE` and `ROOM_ID_FROM_STEP_4_GOES_HERE` with the your own values.

```yaml
matrix_bot_draupnir_enabled: true

matrix_bot_draupnir_access_token: "ACCESS_TOKEN_FROM_STEP_2_GOES_HERE"

matrix_bot_draupnir_management_room: "ROOM_ID_FROM_STEP_4_GOES_HERE"
```

## 5b. Migrating from Mjolnir (Only required if migrating.)

Replace your `matrix_bot_mjolnir` config with `matrix_bot_draupnir` config. Also disable mjolnir if you're doing migration.
That is all you need to do due to that Draupnir can complete migration on its own.

## 6. Installing

After configuring the playbook, run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

You can refer to the upstream [documentation](https://github.com/the-draupnir-project/Draupnir) for additional ways to use and configure draupnir. Check out their [quickstart guide](https://github.com/the-draupnir-project/Draupnir/blob/main/docs/moderators.md#quick-usage) for some basic commands you can give to the bot.

You can configure additional options by adding the `matrix_bot_draupnir_configuration_extension_yaml` variable to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file.

For example to change draupnir's `recordIgnoredInvites` option to `true` you would add the following to your `vars.yml` file.

```yaml
matrix_bot_draupnir_configuration_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_bot_draupnir_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_bot_draupnir_configuration_yaml`.
  recordIgnoredInvites: true
```

## Abuse Reports

Draupnir supports two methods to receive reports in the management room.

The first method intercepts the report API endpoint of the client-server API, which requires integration with the reverse proxy in front of the homeserver.
While this playbook uses reverse proxies, it does not yet implement this.

The other method polls an synapse admin API endpoint and is hence only available when using synapse and when the Draupnir user is an admin user (see step 1).
To enable it, set `pollReports: true` in Draupnir's config:
```yaml
matrix_bot_draupnir_configuration_extension_yaml: |
  pollReports: true
```
