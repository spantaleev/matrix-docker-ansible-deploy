# Setting up Buscarron (optional)

The playbook can install and configure [buscarron](https://gitlab.com/etke.cc/buscarron) for you.

It's a bot you can use to setup **your own helpdesk on matrix**
It's a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) matrix room

## Registering the bot user

By default, the playbook will set up the bot with a username like this: `@bot.buscarron:DOMAIN`.

(to use a different username, adjust the `matrix_bot_buscarron_login` variable).

You **need to register the bot user manually** before setting up the bot. You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.buscarron password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_bot_buscarron_enabled: true

# Adjust this to whatever password you chose when registering the bot user
matrix_bot_buscarron_password: PASSWORD_FOR_THE_BOT

# Adjust accepted forms
matrix_bot_buscarron_forms:
  - name: contact # (mandatory) Your form name, will be used as endpoint, eg: buscarron.DOMAIN/contact
    room: "!yourRoomID:DOMAIN" # (mandatory) Room ID where form submission will be posted
    redirect: https://DOMAIN # (mandatory) To what page user will be redirected after the form submission
    ratelimit: 1r/m # (optional) rate limit of the form, format: <max requests>r/<interval:s,m>, eg: 1r/s or 54r/m
    extensions: [] # (optional) list of form extensions (not used yet)

matrix_bot_buscarron_spam_hosts: [] # (optional) list of email domains/hosts that should be rejected automatically
matrix_bot_buscarron_spam_emails: [] # (optional) list of email addresses that should be rejected automatically
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

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To use the bot, invite the `@bot.buscarron:DOMAIN` to the room you specified in a config, after that any point your form to the form url, example for the `contact` form:

```html
<form method="POST" action="https://buscarron.DOMAIN/contact">
<!--your fields-->
</form>
```

You can also refer to the upstream [documentation](https://gitlab.com/etke.cc/buscarron).
