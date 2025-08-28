<!--
SPDX-FileCopyrightText: 2025 Jason LaGuidice

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Steam bridging (optional)

The playbook can install and configure [matrix-steam-bridge](https://github.com/jasonlaguidice/matrix-steam-bridge) for you.

See the project's [documentation](https://github.com/jasonlaguidice/matrix-steam-bridge/blob/main/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [Steam](https://steampowered.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_steam_bridge_enabled: true
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` and `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

The tag for `just` commands for this bridge is `matrix-steam-bridge` - for example: `just install-service matrix-steam-bridge`

## Usage

To use the bridge, you need to start a chat with `Steam bridge bot` with the handle `@steambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

The bridge supports QR code and password-based login as well as SteamGuard codes via app, SMS, or e-mail. See matrix-steam-bridge [documentation](https://github.com/jasonlaguidice/matrix-steam-bridge) for more information about how to configure the bridge.

To login, send `login [flow ID]` where possible flow IDs are `password` or `qr`

Once logged in, send `search [name]` to search through recognized Steam friends. You can send a user name, display name, or all forms of Steam ID. Send `start-chat [identifier]` to request the bridge bot to open a chat room with a user.

Chat rooms will automatically be opened as new messages are received.

Send `help` to the bot to see the available commands.
