<!--
SPDX-FileCopyrightText: 2020 Tulir Asokan
SPDX-FileCopyrightText: 2021 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up MX Puppet Twitter bridging (optional)

**Note**: bridging to [Twitter](https://twitter.com/) can also happen via the [mautrix-twitter](configuring-playbook-bridge-mautrix-twitter.md) bridge supported by the playbook.

The playbook can install and configure [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) for you.

See the project's [documentation](https://github.com/Sorunome/mx-puppet-twitter/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisite

Make an app on [developer.twitter.com](https://developer.twitter.com/en/apps).

## Adjusting the playbook configuration

To enable the [Twitter](https://twitter.com) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_twitter_enabled: true
matrix_mx_puppet_twitter_consumer_key: ''
matrix_mx_puppet_twitter_consumer_secret: ''
matrix_mx_puppet_twitter_access_token: ''
matrix_mx_puppet_twitter_access_token_secret: ''
matrix_mx_puppet_twitter_environment: ''
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

To use the bridge, you need to start a chat with `Twitter Puppet Bridge` with the handle `@_twitterpuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

To log in, use `link` and click the link.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Send `help` to the bot to see the available commands.
