<!--
SPDX-FileCopyrightText: 2025 - 2026 luschmar
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up a Matrix <-> Meshtastic bridge (optional)

The playbook can install and configure [meshtastic-matrix-relay](https://github.com/jeremiah-k/meshtastic-matrix-relay) (sometimes referred to as `mmrelay`) for you — a bridge between [Matrix](https://matrix.org/) and [Meshtastic](https://meshtastic.org/) mesh networks.

See the [project's documentation](https://github.com/jeremiah-k/meshtastic-matrix-relay) to learn what it does and why it might be useful to you.

## Prerequisites

You need a Matrix account for the bot. You can either [register the bot account manually](registering-users.md) or let the playbook create it when running `ansible-playbook … --tags=ensure-matrix-users-created`. Either way, you'll need the account's **password** to configure the bridge — unlike most other bridges in this playbook, `mmrelay` authenticates with a password and creates its own session (optionally with End-to-End Encryption material).

You also need access to a Meshtastic device, connected to the server via one of:

- **TCP**: the device is reachable on the network (e.g. a Meshtastic node running the TCP API),
- **Serial**: the device is plugged in via USB and available on the host (e.g. `/dev/ttyUSB0`),
- **BLE**: the device is reachable via Bluetooth Low Energy from the host.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_meshtastic_relay_enabled: true

# Password for the bot's Matrix account.
# On first startup, the bridge uses this to log in and persist credentials
# (including End-to-End Encryption material) under its data directory.
# After that, the password can be removed from this variable.
matrix_meshtastic_relay_matrix_bot_password: "PASSWORD_FOR_THE_BOT"

# How the bridge connects to your Meshtastic device.
# One of: tcp, serial, ble
matrix_meshtastic_relay_connection_type: tcp

# For connection_type: tcp
matrix_meshtastic_relay_tcp_host: "meshtastic.local"

# For connection_type: serial
# matrix_meshtastic_relay_serial_port: "/dev/ttyUSB0"

# For connection_type: ble
# matrix_meshtastic_relay_ble_address: "AA:BB:CC:DD:EE:FF"

# Matrix rooms to bridge to Meshtastic channels.
matrix_meshtastic_relay_matrix_rooms_list:
  - id: "#meshtastic:{{ matrix_domain }}"
    meshtastic_channel: "0"
```

By default, the bot's Matrix ID is `@meshtasticbot:{{ matrix_domain }}`. To change it, adjust `matrix_meshtastic_relay_matrix_bot_user_id`.

### Bluetooth (BLE) connections

When `matrix_meshtastic_relay_connection_type` is `ble`, the container runs with `--network=host` and bind-mounts the host's DBus socket — both are required for Bluetooth pairing/communication. Only use this connection type if you trust the playbook-managed host and are comfortable with these privileges.

### Serial connections

When `matrix_meshtastic_relay_connection_type` is `serial`, the host device referenced by `matrix_meshtastic_relay_serial_port` is passed through to the container. Make sure that `matrix_user_uid` / `matrix_user_gid` have read/write access to that device (e.g. by adding the matrix user to the `dialout` group, or adjusting udev rules).

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-meshtastic-relay/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override individual `matrix_meshtastic_relay_*` variables, or make finer-grained adjustments via `matrix_meshtastic_relay_configuration_extension_yaml`.

## Installing

After configuring the playbook, run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`.

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Invite the bot to the Matrix rooms listed in `matrix_meshtastic_relay_matrix_rooms_list` and it will relay between Matrix and the corresponding Meshtastic channel. Messages sent on Meshtastic will appear in Matrix and vice versa.

See the [project's wiki](https://github.com/jeremiah-k/meshtastic-matrix-relay/wiki) for details about commands, plugins and advanced usage.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-meshtastic-relay`.
