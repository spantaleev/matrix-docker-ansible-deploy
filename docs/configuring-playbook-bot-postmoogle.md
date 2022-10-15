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

## Use Postmoogle for sending mails

You will need to add several DNS records
See [Configuring DNS](configuring-dns.md).

To be able to get the value for `!pm dkim` for your DNS settings you need to have admin-rights for the bridge.
If you didn't set this generally for all bridges with:
```yaml
matrix_admin: "@username:{{ matrix_domain }}"
```
you need to set one for administering postmoogle with this item in your `vars.yml`:
```yaml
matrix_bot_postmoogle_admins:
  - "@<username>:{{ matrix_domain }}"
```

If you want to use TLS (you should) and you use `matrix_ssl_retrieval_method: manually-managed`) you have to add to `vars.yml`:
```yaml
### SSL
## on-host SSL dir
matrix_bot_postmoogle_ssl_path: ""

## in-container SSL paths
# matrix_bot_postmoogle_tls_cert is the SSL certificate's certificate.
# This is likely set via group_vars/matrix_servers, so you don't need to set it.
# If you do need to set it manually, note that this is an in-container path.
# To mount a certificates volumes into the container, use matrix_bot_postmoogle_ssl_path
# Example value: /ssl/live/{{ matrix_bot_postmoogle_domain }}/fullchain.pem
matrix_bot_postmoogle_tls_cert: ""

# matrix_bot_postmoogle_tls_key is the SSL certificate's key.
# This is likely set via group_vars/matrix_servers, so you don't need to set it.
# If you do need to set it manually, note that this is an in-container path.
# To mount a certificates volumes into the container, use matrix_bot_postmoogle_ssl_path
# Example value: /ssl/live/{{ matrix_bot_postmoogle_domain }}/privkey.pem
matrix_bot_postmoogle_tls_key: ""
```
**Note:** `matrix_bot_postmoogle_ssl_path:` defaults to what you set for `matrix_ssl_config_dir_path:` As seen in [/group_vars/matrix_servers](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/group_vars/matrix_servers#L1213) but it has to be set again to make postmoogle look for it outside the docker-container.

## Open Ports
If you run a firewall on your server and/or it sits behind a NAT-Router, remember to open/forward the ports `25` (for non-TLS) and `587` (TLS)
as set [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/roles/matrix-bot-postmoogle/defaults/main.yml#L121)

It's possible to change those ports in `vars.yml` with:
```yaml
matrix_bot_postmoogle_smtp_host_bind_port: ""
matrix_bot_postmoogle_submission_host_bind_port: ""
```

If you want to enforce TLS on both ports add this to `vars.yml`:
```yaml
matrix_bot_postmoogle_tls_required: true
```

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
