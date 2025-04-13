<!--
SPDX-FileCopyrightText: 2020 MDAD project contributors
SPDX-FileCopyrightText: 2020 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Matrix SMS bridging (optional)

The playbook can install and configure [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) for you.

See the project's [documentation](https://github.com/benkuly/matrix-sms-bridge/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisite

The bridge uses [android-sms-gateway-server](https://github.com/RebekkaMa/android-sms-gateway-server). You need to configure it first.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_sms_bridge_enabled: true

# (optional but recommended) a room ID to a default room
matrix_sms_bridge_default_room: ""

# (optional but recommended) configure your server location
matrix_sms_bridge_default_region: DE
matrix_sms_bridge_default_timezone: Europe/Berlin

# Settings to connect to android-sms-gateway-server
matrix_sms_bridge_provider_android_baseurl: https://192.168.24.24:9090
matrix_sms_bridge_provider_android_username: admin
matrix_sms_bridge_provider_android_password: supeSecretPassword

# (optional) if your android-sms-gateway-server uses a self signed vertificate, the bridge needs a "truststore". This can be the certificate itself.
matrix_sms_bridge_provider_android_truststore_local_path: android-sms-gateway-server.p12
matrix_sms_bridge_provider_android_truststore_password: 123
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-sms/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_sms_bridge_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Read the [user guide](https://github.com/benkuly/matrix-sms-bridge/blob/master/README.md#user-guide) to see how this bridge works.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-sms-bridge`.
