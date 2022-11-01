# Setting up Buscarron (optional)

The playbook can install and configure [buscarron](https://gitlab.com/etke.cc/buscarron) for you.

It's a bot you can use to setup **your own helpdesk on matrix**
It's a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) matrix room


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_buscarron_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_buscarron_login: bot.buscarron

# Generate a strong password here. Consider generating it with `pwgen -s 64 1`
matrix_bot_buscarron_password: PASSWORD_FOR_THE_BOT

# Adjust accepted forms
matrix_bot_buscarron_forms:
  - name: contact # (mandatory) Your form name, will be used as endpoint, eg: buscarron.DOMAIN/contact
    room: "!yourRoomID:DOMAIN" # (mandatory) Room ID where form submission will be posted
    redirect: https://DOMAIN # (mandatory) To what page user will be redirected after the form submission
    ratelimit: 1r/m # (optional) rate limit of the form, format: <max requests>r/<interval:s,m>, eg: 1r/s or 54r/m
    hasemail: 1 # (optional) form has "email" field that should be validated
    extensions: [] # (optional) list of form extensions (not used yet)

matrix_bot_buscarron_spamlist: [] # (optional) list of emails/domains/hosts (with wildcards support) that should be rejected automatically
```

You will also need to add a DNS record so that buscarron can be accessed.
By default buscarron will use https://buscarron.DOMAIN so you will need to create an CNAME record for `buscarron`.
See [Configuring DNS](configuring-dns.md).

If you would like to use a different domain, add the following to your configuration file (changing it to use your preferred domain):

```yaml
matrix_server_fqn_buscarron: "form.{{ matrix_domain }}"
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- the `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account

- if you change the bot password (`matrix_bot_buscarron_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_buscarron_password` to let the bot know its new password


## Usage

To use the bot, invite the `@bot.buscarron:DOMAIN` to the room you specified in a config, after that any point your form to the form url, example for the `contact` form:

```html
<form method="POST" action="https://buscarron.DOMAIN/contact">
<!--your fields-->
</form>
```

You can also refer to the upstream [documentation](https://gitlab.com/etke.cc/buscarron).
