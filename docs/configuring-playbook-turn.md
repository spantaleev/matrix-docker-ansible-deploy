<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Christian Wolf
SPDX-FileCopyrightText: 2020 MDAD project contributors
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring a TURN server (optional, advanced)

By default, this playbook installs and configures the [coturn](https://github.com/coturn/coturn) as a TURN server, through which clients can make audio/video calls even from [NAT](https://en.wikipedia.org/wiki/Network_address_translation)-ed networks. It also configures the Synapse chat server by default, so that it points to the coturn TURN server installed by the playbook. If that's okay, you can skip this document.

If you'd like to stop the playbook installing the server, see the section [below](#disabling-coturn) to check the configuration for disabling it.

## Adjusting the playbook configuration

### Define public IP manually (optional)

In the `hosts` file we explicitly ask for your server's external IP address when defining `ansible_host`, because the same value is used for configuring coturn.

If you'd rather use a local IP for `ansible_host`, add the following configuration to your `vars.yml` file. Make sure to replace `YOUR_PUBLIC_IP` with the pubic IP used by the server.

```yaml
matrix_coturn_turn_external_ip_address: "YOUR_PUBLIC_IP"
```

If you'd like to rely on external IP address auto-detection (not recommended unless you need it), set an empty value to the variable. The playbook will automatically contact an [EchoIP](https://github.com/mpolden/echoip)-compatible service (`https://ifconfig.co/json` by default) to determine your server's IP address. This API endpoint is configurable via the `matrix_coturn_turn_external_ip_address_auto_detection_echoip_service_url` variable.

If your server has multiple external IP addresses, the coturn role offers a different variable for specifying them:

```yaml
# Note: matrix_coturn_turn_external_ip_addresses is different than matrix_coturn_turn_external_ip_address
matrix_coturn_turn_external_ip_addresses: ['1.2.3.4', '4.5.6.7']
```

### Change the authentication mechanism (optional)

The playbook uses the [`auth-secret` authentication method](https://github.com/coturn/coturn/blob/873cabd6a2e5edd7e9cc5662cac3ffe47fe87a8e/README.turnserver#L186-L199) by default, but you may switch to the [`lt-cred-mech` method](https://github.com/coturn/coturn/blob/873cabd6a2e5edd7e9cc5662cac3ffe47fe87a8e/README.turnserver#L178) which [some report](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3191) to be working better.

To do so, add the following configuration to your `vars.yml` file:

```yaml
matrix_coturn_authentication_method: lt-cred-mech
```

Regardless of the selected authentication method, the playbook generates secrets automatically and passes them to the homeserver and coturn.

If [Jitsi](configuring-playbook-jitsi.md) is installed, note that switching to `lt-cred-mech` will disable the integration between Jitsi and your coturn server, as Jitsi seems to support the `auth-secret` authentication method only.

### Use your own external coturn server (optional)

If you'd like to use another TURN server (be it coturn or some other one), add the following configuration to your `vars.yml` file. Make sure to replace `HOSTNAME_OR_IP` with your own.

```yaml
# Disable integrated coturn server
matrix_coturn_enabled: false

# Point Synapse to your other coturn server
matrix_synapse_turn_uris:
- turns:HOSTNAME_OR_IP?transport=udp
- turns:HOSTNAME_OR_IP?transport=tcp
- turn:HOSTNAME_OR_IP?transport=udp
- turn:HOSTNAME_OR_IP?transport=tcp
```

If you have or want to enable Jitsi, you might want to enable the TURN server there too. If you do not do it, Jitsi will fall back to an upstream service.

```yaml
jitsi_web_stun_servers:
- stun:HOSTNAME_OR_IP:PORT
```

You can put multiple host/port combinations if you'd like to.

### Edit the reloading schedule (optional)

By default the service is reloaded on 6:30 a.m. every day based on the `matrix_coturn_reload_schedule` variable so that new SSL certificates can kick in. It is defined in the format of systemd timer calendar.

To edit the schedule, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
matrix_coturn_reload_schedule: "*-*-* 06:30:00"
```

**Note**: the actual job may run with a delay. See `matrix_coturn_reload_schedule_randomized_delay_sec` for its default value.

### Extending the configuration

There are some additional things you may wish to configure about the TURN server.

Take a look at:

- `roles/custom/matrix-coturn/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Disabling coturn

If, for some reason, you'd like for the playbook to not install coturn (or to uninstall it if it was previously installed), add the following configuration to your `vars.yml` file:

```yaml
matrix_coturn_enabled: false
```

In that case, Synapse would not point to any coturn servers and audio/video call functionality may fail.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-coturn`.
