# Setting up Buscarron (optional)

The playbook can install and configure [buscarron](https://github.com/etkecc/buscarron) for you.

Buscarron is bot that receives HTTP POST submissions of web forms and forwards them to a Matrix room.


## Decide on a domain and path

By default, Buscarron is configured to use its own dedicated domain (`buscarron.DOMAIN`) and requires you to [adjust your DNS records](#adjusting-dns-records).

You can override the domain and path like this:

```yaml
# Switch to the domain used for Matrix services (`matrix.DOMAIN`),
# so we won't need to add additional DNS records for Buscarron.
matrix_bot_buscarron_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /buscarron subpath
matrix_bot_buscarron_path_prefix: /buscarron
```


## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Buscarron domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.


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

**NOTE**: to fight against spam, Buscarron is **very aggressive when it comes to banning** and will ban you if:

- if you hit the homepage (HTTP `GET` request to `/`)
- if you submit a form to the wrong URL (`POST` request to `/non-existing-form`)
- if `hasemail` is enabled for the form (like in the example above) and you don't submit an `email` field

If you get banned, you'd need to restart the process by running the playbook with `--tags=start` or running `systemctl restart matrix-bot-buscarron` on the server.

You can also refer to the upstream [documentation](https://github.com/etkecc/buscarron).
