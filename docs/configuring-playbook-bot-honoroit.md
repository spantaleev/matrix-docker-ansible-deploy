# Setting up Honoroit (optional)

The playbook can install and configure [Honoroit](https://gitlab.com/etke.cc/honoroit) for you.

It's a bot you can use to setup **your own helpdesk on matrix**

See the project's [documentation](https://gitlab.com/etke.cc/honoroit#how-it-looks-like) to learn what it does with screenshots and why it might be useful to you.


## Registering the bot user

By default, the playbook will set up the bot with a username like this: `@honoroit:DOMAIN`.

(to use a different username, adjust the `matrix_bot_honoroit_login` variable).

You **need to register the bot user manually** before setting up the bot. You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=honoroit password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_honoroit_enabled: true

# Adjust this to whatever password you chose when registering the bot user
matrix_bot_honoroit_password: PASSWORD_FOR_THE_BOT

# Adjust this to your room ID
matrix_bot_honoroit_roomid: "!yourRoomID:DOMAIN"
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, invite the `@honoroit:DOMAIN` to the room you specified in config, after that any matrix user can send a message to the `@honoroit:DOMAIN` to start a new thread in that room.

Send `!ho help` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [documentation](https://gitlab.com/etke.cc/honoroit#features).
