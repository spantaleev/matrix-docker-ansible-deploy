<!--
SPDX-FileCopyrightText: 2020 - 2021 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Hugues Morisset
SPDX-FileCopyrightText: 2020 Panagiotis Vasilopoulos
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up MX Puppet Steam bridging (optional, deprecated)

**Note**: This bridge has been deprecated in favor of the [matrix-steam-bridge](https://github.com/jasonlaguidice/matrix-steam-bridge) bridge for Steam, which can be [installed using this playbook](configuring-playbook-bridge-steam.md). Consider using that bridge instead of this one.

The playbook can install and configure [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) for you.

See the project's [documentation](https://github.com/icewind1991/mx-puppet-steam/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [Steam](https://steampowered.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_steam_enabled: true
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `Steam Puppet Bridge` with the handle `@_steampuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token. See mx-puppet-steam [documentation](https://github.com/icewind1991/mx-puppet-steam) for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Send `help` to the bot to see the available commands.
