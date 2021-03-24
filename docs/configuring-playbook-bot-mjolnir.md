# Setting up Mjolnir (optional)

The playbook can install and configure [Mjolnir](https://github.com/matrix-org/mjolnir) for you.

Mjolnir is a moderation tool for Matrix.

See the project's [documentation](https://github.com/matrix-org/mjolnir) to learn what it does and why it might be useful to you.


## Registering the bot user

The playbook does not automatically create users for you. The bot requires at least 1 access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.mjolnir password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```


## Getting an access token

If you use curl, you can get an access token like this:

```
curl -X POST --header 'Content-Type: application/json' -d '{
    "identifier": { "type": "m.id.user", "user": "bot.mjolnir" },
    "password": "PASSWORD_FOR_THE_BOT",
    "type": "m.login.password"
}' 'https://matrix.YOURDOMAIN/_matrix/client/r0/login'
```

Alternatively, you can use a full-featured client (such as Element) to log in and get the access token from there (note: don't log out from the client as that will invalidate the token), but doing so might lead to decryption problems. That warning comes from [here](https://github.com/matrix-org/go-neb#quick-start).


## Make sure account is free from rate limiting

TODO

```
insert into ratelimit_override values ("@bot.mjolnir:DOMAIN", 0, 0);
```

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

```yaml
TODO
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

TODO

You can also refer to the upstream [documentation](https://github.com/matrix-org/mjolnir).
