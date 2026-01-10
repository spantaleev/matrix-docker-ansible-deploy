<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Prometheus Alertmanager integration via matrix-alertmanager-receiver (optional)

The playbook can install and configure the [matrix-alertmanager-receiver](https://github.com/metio/matrix-alertmanager-receiver) service for you. It's a [client](https://prometheus.io/docs/alerting/latest/clients/) for Prometheus' [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/), allowing you to deliver alerts to Matrix rooms.

See the project's [documentation](https://github.com/metio/matrix-alertmanager-receiver/blob/main/README.md) to learn what it does and why it might be useful to you.

This service is meant to be used with an external [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) instance. It's **not** meant to be integrated with the [Prometheus & Grafana stack](./configuring-playbook-prometheus-grafana.md) installed by this playbook, because the Alertmanager component is not installed by it.

## Prerequisites

### Register the bot account

This service uses a bot (with a username specified in `matrix_alertmanager_receiver_config_matrix_user_id_localpart`) for delivering messages.

The playbook does not automatically create users for you. You **need to register the bot user manually** before setting up the bot.

Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.alertmanager.receiver password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

### Obtain an access token

The bot requires an access token to be able to connect to your homeserver. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

> [!WARNING]
> Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

### Join to rooms as the bot manually

ℹ️ **This bot does not accept room invitations automatically**. To deliver messages to rooms, the bot must be joined to all rooms manually.

For each new room you would like the bot to deliver alerts to, invite the bot to the room.

Then, log in as the bot using any Matrix client of your choosing, accept the room invitation from the bot's account, and log out.

## Adjusting DNS records (optional)

By default, this playbook installs matrix-alertmanager-receiver on the `matrix.` subdomain, at the `/matrix-alertmanager-receiver` path (https://matrix.example.com/matrix-alertmanager-receiver). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-matrix-alertmanager-receiver-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `ACCESS_TOKEN_HERE` with the one created [above](#obtain-an-access-token).

```yaml
matrix_alertmanager_receiver_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_alertmanager_receiver_config_matrix_user_id_localpart: "bot.alertmanager.receiver"

matrix_alertmanager_receiver_config_matrix_access_token: "ACCESS_TOKEN_HERE"

# Optionally, configure some mappings (URL-friendly room name -> actual Matrix room ID).
#
# If you don't configure mappings, you can still deliver alerts using URLs like this:
# https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/!qporfwt:example.com
#
# If a mapping like the one below is configured, you can deliver alerts using friendlier URLs like this:
# https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/some-room-name
matrix_alertmanager_receiver_config_matrix_room_mapping:
  some-room-name: "!qporfwt:{{ matrix_domain }}"
```

### Adjusting the matrix-alertmanager-receiver URL (optional)

By tweaking the `matrix_alertmanager_receiver_hostname` and `matrix_alertmanager_receiver_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_alertmanager_receiver_hostname: alertmanager.example.com
matrix_alertmanager_receiver_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the matrix-alertmanager-receiver domain (`alertmanager.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-alertmanager-receiver/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-alertmanager-receiver/templates/config.yaml.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_alertmanager_receiver_configuration_extension_yaml` variable

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Configure your Prometheus Alertmanager with configuration like this:

```yaml
receivers:
  - name: matrix
    webhook_configs:
      - send_resolved: true
        url: URL_HERE
route:
  group_by:
    - namespace
  group_interval: 5m
  group_wait: 30s
  receiver: "matrix"
  repeat_interval: 12h
  routes:
    - receiver: matrix
```

where `URL_HERE` looks like `https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/some-room-name` or `https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/!qporfwt:example.com`.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-alertmanager-receiver`.

### Increase logging verbosity

The default logging level for this component is `info`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: error, warn, info, debug
matrix_alertmanager_receiver_container_process_argument_log_level: debug
```
