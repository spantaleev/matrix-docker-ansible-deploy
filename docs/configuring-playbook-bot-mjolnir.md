# Setting up Mjolnir (optional)

The playbook can install and configure the [Mjolnir](https://github.com/matrix-org/mjolnir) moderation bot for you.

See the project's [documentation](https://github.com/matrix-org/mjolnir) to learn what it does and why it might be useful to you.

Note: the playbook does not currently support the Mjolnir Synapse module. The playbook does support another antispam module, see [Setting up Synapse Simple Antispam](configuring-playbook-synapse-simple-antispam.md).


## 1. Register the bot account

The playbook does not automatically create users for you. The bot requires an access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.mjolnir password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

If you would like Mjolnir to be able to deactivate users, move aliases, shutdown rooms, etc then it must be a server admin so you need to change `admin=no` to `admin=yes` in the command above.


## 2. Get an access token

If you use curl, you can get an access token like this:

```
curl -X POST --header 'Content-Type: application/json' -d '{
    "identifier": { "type": "m.id.user", "user": "bot.mjolnir" },
    "password": "PASSWORD_FOR_THE_BOT",
    "type": "m.login.password"
}' 'https://matrix.DOMAIN/_matrix/client/r0/login'
```

Alternatively, you can use a full-featured client (such as Element) to log in and get the access token from there (note: don't log out from the client as that will invalidate the token).


## 3. Make sure the account is free from rate limiting

You will need to prevent Synapse from rate limiting the bot's account. This is not an optional step. If you do not do this step Mjolnir will crash. [Currently there is no Synapse config option for this](https://github.com/matrix-org/synapse/issues/6286) so you have to manually edit the Synapse database. Manually editing the Synapse database is rarely a good idea but in this case it is required. Please ask for help if you are uncomfortable with these steps.

1. Copy the statement below into a text editor. 

	```
	INSERT INTO ratelimit_override VALUES ("@bot.mjolnir:DOMAIN", 0, 0);
	```

1. Change the username (`@bot.mjolnir:DOMAIN`) to the username you used when you registered the bot's account. You must change `DOMAIN` to your server's domain.

1. Get a database terminal by following these steps: [maintenance-postgres.md#getting-a-database-terminal](maintenance-postgres.md#getting-a-database-terminal)

1. Connect to Synapse's database by typing `\connect synapse` into the database terminal

1. Paste in the `INSERT INTO` command that you edited and press enter.

You can run `SELECT * FROM ratelimit_override;` to see if it worked. If the output looks like this:

```
      user_id          | messages_per_second | burst_count
-----------------------+---------------------+-------------
 @bot.mjolnir:raim.ist |                   0 |           0`
```
then you did it correctly.


## 4. Create a management room

Using your own account, create a new invite only room that you will use to manage the bot. This is the room where you will see the status of the bot and where you will send commands to the bot, such as the command to ban a user from another room. Anyone in this room can control the bot so it is important that you only invite trusted users to this room. The room must be unencrypted since the playbook does not support installing Pantalaimon yet.

Once you have created the room you need to copy the room ID so you can tell the bot to use that room. In Element you can do this by going to the room's settings, clicking Advanced, and then coping the internal room ID. The room ID will look something like `!QvgVuKq0ha8glOLGMG:DOMAIN`.

Finally invite the `@bot.mjolnir:DOMAIN` account you created earlier into the room.


## 5. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

You must replace `ACCESS_TOKEN_FROM_STEP_2_GOES_HERE` and `ROOM_ID_FROM_STEP_4_GOES_HERE` with the your own values.

```yaml
matrix_bot_mjolnir_enabled: true

matrix_bot_mjolnir_access_token: "ACCESS_TOKEN_FROM_STEP_2_GOES_HERE"

matrix_bot_mjolnir_management_room: "ROOM_ID_FROM_STEP_4_GOES_HERE"
```


## 6. Installing

After configuring the playbook, run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

You can refer to the upstream [documentation](https://github.com/matrix-org/mjolnir) for additional ways to use and configure mjolnir. Check out their [quickstart guide](https://github.com/matrix-org/mjolnir#quickstart-guide) for some basic commands you can give to the bot.

You can configure additional options by adding the `matrix_bot_mjolnir_configuration_extension_yaml` variable to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file.

For example to change mjolnir's `recordIgnoredInvites` option to `true` you would add the following to your `vars.yml` file.

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
