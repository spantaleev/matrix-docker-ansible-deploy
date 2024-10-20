# Setting up Honoroit (optional)

The playbook can install and configure [Honoroit](https://github.com/etkecc/honoroit) for you.

It's a bot you can use to setup **your own helpdesk on matrix**

See the project's [documentation](https://github.com/etkecc/honoroit#how-it-looks-like) to learn what it does with screenshots and why it might be useful to you.


## Adjusting the playbook configuration

To enable Honoroit, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_honoroit_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_honoroit_login: honoroit

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_honoroit_password: PASSWORD_FOR_THE_BOT

# Adjust this to your room ID
matrix_bot_honoroit_roomid: "!yourRoomID:{{ matrix_domain }}"
```

### Adjusting the Honoroit URL

By default, this playbook installs Honoroit on the `matrix.` subdomain, at the `/honoroit` path (https://matrix.example.com/honoroit). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_bot_honoroit_hostname` and `matrix_bot_honoroit_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_bot_honoroit_hostname: honoroit.example.com
matrix_bot_honoroit_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the Honoroit domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook, run the [installation](installing.md) command:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- the `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account

- if you change the bot password (`matrix_bot_honoroit_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_honoroit_password` to let the bot know its new password


## Usage

To use the bot, invite the `@honoroit:example.com` to the room you specified in config, after that any Matrix user can send a message to the `@honoroit:example.com` to start a new thread in that room.

Send `!ho help` to the room to see the bot's help menu for additional commands.

You can also refer to the upstream [documentation](https://github.com/etkecc/honoroit#features).
