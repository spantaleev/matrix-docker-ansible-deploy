# Setting up matrix-alertmanager-receiver (optional)

The playbook can install and configure the [matrix-alertmanager-receiver](https://github.com/metio/matrix-alertmanager-receiver) service for you. It's a [client](https://prometheus.io/docs/alerting/latest/clients/) for Prometheus' [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/), allowing you to deliver alerts to Matrix rooms.

See the project's [documentation](https://github.com/metio/matrix-alertmanager-receiver) to learn more about what this component does and why it might be useful to you.

At the moment, **setting up this service's bot requires some manual actions** as described below in [Account and room preparation](#account-and-room-preparation).

This service is meant to be used with an external [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) instance. It's **not** meant to be integrated with the [Prometheus & Grafana stack](./configuring-playbook-prometheus-grafana.md) installed by this playbook, because the Alertmanager component is not installed by it.

## Adjusting the playbook configuration

To enable matrix-alertmanager-receiver, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yml
matrix_alertmanager_receiver_enabled: true

# If you'd like to change the username for this bot, uncomment and adjust. Otherwise, remove.
# matrix_alertmanager_receiver_config_matrix_user_id_localpart: "bot.alertmanager.receiver"

# Specify the bot user's access token here.
# See the "Account and room preparation" section below.
matrix_alertmanager_receiver_config_matrix_access_token: ''

# Optionally, configure some mappings (URL-friendly room name -> actual Matrix room ID).
#
# If you don't configure mappings, you can still deliver alerts using URLs like this:
# https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/!some-room-id:example.com
#
# If a mapping like the one below is configured, you can deliver alerts using friendlier URLs like this:
# https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/some-room-name
matrix_alertmanager_receiver_config_matrix_room_mapping:
  some-room-name: "!some-room-id:{{ matrix_domain }}"
```

See `roles/custom/matrix-alertmanager-receiver/defaults/main.yml` for additional configuration variables.

### Adjusting the matrix-alertmanager-receiver URL

By default, this playbook installs matrix-alertmanager-receiver on the `matrix.` subdomain, at the `/matrix-alertmanager-receiver` path (https://matrix.example.com/matrix-alertmanager-receiver). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_alertmanager_receiver_hostname` and `matrix_alertmanager_receiver_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_alertmanager_receiver_hostname: alertmanager.example.com
matrix_alertmanager_receiver_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the matrix-alertmanager-receiver domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Account and room preparation

The playbook can automatically create users, but it cannot automatically obtain access tokens, nor perform any of the other manual actions below.

`matrix-alertmanager-receiver` uses a bot (with a username specified in `matrix_alertmanager_receiver_config_matrix_user_id_localpart` - see above) for delivering messages. You need to **manually register this bot acccount and obtain an access token for it**.

1. [Register a new user](registering-users.md): `ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.alertmanager.receiver password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user`
2. [Obtain an access token](obtaining-access-tokens.md) for the bot's user account
3. Invite the bot to a room where you'd like to alerts to be delivered
4. Log in as the bot using any Matrix client of your choosing, accept the room invitation from the bot's account and log out
5. (Optionally) Adjust `matrix_alertmanager_receiver_config_matrix_room_mapping` to create a mapping between the new room and its ID

Steps 1 and 2 above only need to be done once, while preparing your [configuration](#configuration).

Steps 3 and 4 need to be done for each new room you'd like the bot to deliver alerts to. Step 5 is optional and provides cleaner `/alert/` URLs.


## Installing

Now that you've [prepared the bot account and room](#account-and-room-preparation), [configured the playbook](#configuration), and potentially [adjusted your DNS records](#adjusting-dns-records), you can run the [installation](installing.md) command: `just install-all`

Then, you can proceed to [Usage](#usage).


## Usage

Configure your Prometheus Alertmanager with configuration like this:

```yml
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

.. where `URL_HERE` looks like `https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/some-room-name` or `https://matrix.example.com/matrix-alertmanager-receiver-RANDOM_VALUE_HERE/alert/!some-room-id:example.com`.

This bot does **not** accept room invitations automatically (like many other bots do). To deliver messages to rooms, **the bot must be joined to all rooms manually** - see Step 5 of the [Account and room preparation](#account-and-room-preparation) section.
