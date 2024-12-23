# Setting up Buscarron (optional)

The playbook can install and configure [Buscarron](https://github.com/etkecc/buscarron) for you.

Buscarron is bot that receives HTTP POST submissions of web forms and forwards them to a Matrix room.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_buscarron_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_buscarron_login: bot.buscarron

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_bot_buscarron_password: PASSWORD_FOR_THE_BOT

# Adjust accepted forms
matrix_bot_buscarron_forms:
  - name: contact # (mandatory) Your form name, will be used as endpoint, eg: buscarron.example.com/contact
    room: "!qporfwt:{{ matrix_domain }}" # (mandatory) Room ID where form submission will be posted
    redirect: https://example.com # (mandatory) To what page user will be redirected after the form submission
    ratelimit: 1r/m # (optional) rate limit of the form, format: <max requests>r/<interval:s,m>, eg: 1r/s or 54r/m
    hasemail: 1 # (optional) form has "email" field that should be validated
    extensions: [] # (optional) list of form extensions (not used yet)

matrix_bot_buscarron_spamlist: [] # (optional) list of emails/domains/hosts (with wildcards support) that should be rejected automatically
```

### Adjusting the Buscarron URL

By default, this playbook installs Buscarron on the `buscarron.` subdomain (`buscarron.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_bot_buscarron_hostname` and `matrix_bot_buscarron_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Buscarron.
matrix_bot_buscarron_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /buscarron subpath
matrix_bot_buscarron_path_prefix: /buscarron
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Buscarron domain to the Matrix server.

By default, you will need to create a CNAME record for `buscarron`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

- If you change the bot password (`matrix_bot_buscarron_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_buscarron_password` to let the bot know its new password.

## Usage

To use the bot, invite it to the room you specified on your `vars.yml` file (`/invite @bot.buscarron:example.com` where `example.com` is your base domain, not the `matrix.` domain).

After the bot joins the room, anyone can call the web form via HTTP POST method.

Here is an example for the `contact` form:

```html
<form method="POST" action="https://buscarron.example.com/contact">
<!--your fields-->
</form>
```

**Note**: to fight against spam, Buscarron is **very aggressive when it comes to banning** and will ban you if:

- you hit the homepage (HTTP `GET` request to `/`)
- you submit a form to the wrong URL (`POST` request to `/non-existing-form`)
- `hasemail` is enabled for the form (like in the example above) and you don't submit an `email` field

If you get banned, you'd need to restart the process by running the playbook with `--tags=start` or running `systemctl restart matrix-bot-buscarron` on the server.

You can also refer to the upstream [documentation](https://github.com/etkecc/buscarron).
