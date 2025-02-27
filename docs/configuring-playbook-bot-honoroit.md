<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Honoroit (optional)

The playbook can install and configure [Honoroit](https://github.com/etkecc/honoroit) for you.

It's a bot you can use to setup **your own helpdesk on matrix**

See the project's [documentation](https://github.com/etkecc/honoroit/blob/main/README.md) to learn what it does and why it might be useful to you.

## Adjusting DNS records (optional)

By default, this playbook installs Honoroit on the `matrix.` subdomain, at the `/honoroit` path (https://matrix.example.com/honoroit). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-honoroit-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_honoroit_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_honoroit_login: honoroit

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
matrix_bot_honoroit_password: PASSWORD_FOR_THE_BOT

# Adjust this to your room ID
matrix_bot_honoroit_roomid: "!qporfwt:{{ matrix_domain }}"
```

### Adjusting the Honoroit URL (optional)

By tweaking the `matrix_bot_honoroit_hostname` and `matrix_bot_honoroit_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_bot_honoroit_hostname: honoroit.example.com
matrix_bot_honoroit_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Honoroit domain (`honoroit.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-honoroit/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

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

- If you change the bot password (`matrix_bot_honoroit_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_honoroit_password` to let the bot know its new password.

## Usage

To use the bot, invite it to the room you specified on your `vars.yml` file (`/invite @honoroit:example.com` where `example.com` is your base domain, not the `matrix.` domain).

After the bot joins the room, any Matrix user can send a message to it to start a new thread in that room.

Send `!ho help` to the bot in the room to see the available commands.

You can also refer to the upstream [documentation](https://github.com/etkecc/honoroit#features).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bot-honoroit`.

### Increase logging verbosity

If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_bot_honoroit_loglevel: 'DEBUG'
```
