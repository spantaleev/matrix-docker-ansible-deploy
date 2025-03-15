<!--
SPDX-FileCopyrightText: 2020 - 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Rodrigo Belem
SPDX-FileCopyrightText: 2021 Marcel Ackermann
SPDX-FileCopyrightText: 2022 Jim Myhrberg
SPDX-FileCopyrightText: 2022 Nikita Chernyi
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up MX Puppet Slack bridging (optional)

**Note**: bridging to [Slack](https://slack.com) can also happen via the [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) and [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) bridges supported by the playbook. Note that `matrix-appservice-slack` is not available for new installation unless you have already created a classic Slack application, because the creation of classic Slack applications, which this bridge makes use of, has been discontinued.

The playbook can install and configure [mx-puppet-slack](https://gitlab.com/mx-puppet/slack/mx-puppet-slack) for you.

See the project's [documentation](https://gitlab.com/mx-puppet/slack/mx-puppet-slack/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisite

Follow the [OAuth credentials](https://gitlab.com/mx-puppet/slack/mx-puppet-slack#option-2-oauth) instructions to create a new Slack app, setting the redirect URL to `https://matrix.example.com/slack/oauth`.

## Adjusting the playbook configuration

To enable the [Slack](https://slack.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_slack_enabled: true
# Client ID must be quoted so YAML does not parse it as a float.
matrix_mx_puppet_slack_oauth_client_id: "<SLACK_APP_CLIENT_ID>"
matrix_mx_puppet_slack_oauth_client_secret: "<SLACK_APP_CLIENT_SECRET>"
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

To use the bridge, you need to start a chat with `Slack Puppet Bridge` with the handle `@_slackpuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token. See mx-puppet-slack [documentation](https://gitlab.com/mx-puppet/slack/mx-puppet-slack) for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Send `help` to the bot to see the available commands.
