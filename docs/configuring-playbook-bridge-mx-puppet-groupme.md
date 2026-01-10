<!--
SPDX-FileCopyrightText: 2021 Cody Neiman
SPDX-FileCopyrightText: 2021 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Cody Wyatt Neiman
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up MX Puppet GroupMe bridging (optional)

The playbook can install and configure [mx-puppet-groupme](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme) for you.

See the project's [documentation](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [GroupMe](https://groupme.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_groupme_enabled: true
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

To use the bridge, you need to start a chat with `GroupMe Puppet Bridge` with the handle `@_groupmepuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

One authentication method is available.

To link your GroupMe account, go to [dev.groupme.com](https://dev.groupme.com/), sign in, and select "Access Token" from the top menu. Copy the token and message the bridge with:

```
link <access token>
```

Once logged in, send `listrooms` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Send `help` to the bot to see the available commands.
