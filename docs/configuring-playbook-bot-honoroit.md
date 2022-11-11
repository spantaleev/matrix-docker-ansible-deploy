# Setting up Honoroit (optional)

The playbook can install and configure [Honoroit](https://gitlab.com/etke.cc/honoroit) for you.

It's a bot you can use to setup **your own helpdesk on matrix**

See the project's [documentation](https://gitlab.com/etke.cc/honoroit#how-it-looks-like) to learn what it does with screenshots and why it might be useful to you.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_honoroit_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_honoroit_login: honoroit

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_honoroit_password: PASSWORD_FOR_THE_BOT

# Adjust this to your room ID
matrix_bot_honoroit_roomid: "!yourRoomID:DOMAIN"
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- the `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account

- if you change the bot password (`matrix_bot_honoroit_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_honoroit_password` to let the bot know its new password


## Usage

To use the bot, invite the `@honoroit:DOMAIN` to the room you specified in config, after that any matrix user can send a message to the `@honoroit:DOMAIN` to start a new thread in that room.

Send `!ho help` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [documentation](https://gitlab.com/etke.cc/honoroit#features).
