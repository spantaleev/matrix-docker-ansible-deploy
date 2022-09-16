# Setting up Postmoogle (optional)

**Note**: email bridging can also happen via the [email2matrix](configuring-playbook-email2matrix.md) bridge supported by the playbook.

The playbook can install and configure [Postmoogle](https://gitlab.com/etke.cc/postmoogle) for you.

It's a bot/bridge you can use to forward emails to Matrix rooms

See the project's [documentation](https://gitlab.com/etke.cc/postmoogle) to learn what it does and why it might be useful to you.


## Registering the bot user

By default, the playbook will set up the bot with a username like this: `@postmoogle:DOMAIN`.

(to use a different username, adjust the `matrix_bot_postmoogle_login` variable).

You **need to register the bot user manually** before setting up the bot. You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=postmoogle password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_postmoogle_enabled: true

# Adjust this to whatever password you chose when registering the bot user
matrix_bot_postmoogle_password: PASSWORD_FOR_THE_BOT
```

You will also need to add several DNS records so that postmoogle can send emails.
See [Configuring DNS](configuring-dns.md).


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, invite the `@postmoogle:DOMAIN` into a room you want to use as a mailbox.

Then send `!pm mailbox NAME` to expose this Matrix room as an inbox with the email address `NAME@matrix.domain`. Emails sent to that email address will be forwarded to the room.

Send `!pm help` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [documentation](https://gitlab.com/etke.cc/postmoogle).
