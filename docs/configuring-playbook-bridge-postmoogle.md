<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Luke D Iremadze
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Postmoogle email bridging (optional)

The playbook can install and configure [Postmoogle](https://github.com/etkecc/postmoogle) for you.

Postmoogle is a bridge you can use to have its bot user forward emails to Matrix rooms. It runs an SMTP email server and allows you to assign mailbox addresses to the rooms.

See the project's [documentation](https://github.com/etkecc/postmoogle/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

Open the following ports on your server to be able to receive incoming emails:

  - `25/tcp`: SMTP
  - `587/tcp`: Submission (TLS-encrypted SMTP)

If you don't open these ports, you will still be able to send emails, but not receive any.

These port numbers are configurable via the `matrix_postmoogle_smtp_host_bind_port` and `matrix_postmoogle_submission_host_bind_port` variables, but other email servers will try to deliver on these default (standard) ports, so changing them is of little use.

## Adjusting DNS records

To make Postmoogle enable its email sending features, you need to configure MX and TXT (SPF, DMARC, and DKIM) records. See the table below for values which need to be specified.

| Type | Host                           | Priority | Weight | Port | Target                             |
|------|--------------------------------|----------|--------|------|------------------------------------|
| MX   | `matrix`                       | 10       | 0      | -    | `matrix.example.com`               |
| TXT  | `matrix`                       | -        | -      | -    | `v=spf1 ip4:matrix-server-IP -all` |
| TXT  | `_dmarc.matrix`                | -        | -      | -    | `v=DMARC1; p=quarantine;`          |
| TXT  | `postmoogle._domainkey.matrix` | -        | -      | -    | get it from `!pm dkim`             |

**Note**: the DKIM record can be retrieved after configuring and installing the bridge's bot.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_postmoogle_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_postmoogle_login: postmoogle

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_postmoogle_password: PASSWORD_FOR_THE_BOT

# Uncomment to add one or more admins to this bridge:
#
# matrix_postmoogle_admins:
#  - '@yourAdminAccount:{{ matrix_domain }}'
#
# … unless you've made yourself an admin of all bots/bridges like this:
#
# matrix_admin: '@yourAdminAccount:{{ matrix_domain }}'
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-postmoogle/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create a user account of the bridge's bot.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

- If you change the bridge's bot password (`matrix_postmoogle_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_postmoogle_password` to let the bot know its new password.

## Usage

To use the bridge, invite the `@postmoogle:example.com` bot user into a room you want to use as a mailbox.

Then send `!pm mailbox NAME` to expose this Matrix room as an inbox with the email address `NAME@matrix.example.com`. Emails sent to that email address will be forwarded to the room.

Send `!pm help` to the bot in the room to see the available commands.

You can also refer to the upstream [documentation](https://github.com/etkecc/postmoogle).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-postmoogle`.

### Increase logging verbosity

The default logging level for this component is `INFO`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_postmoogle_loglevel: 'DEBUG'
```
