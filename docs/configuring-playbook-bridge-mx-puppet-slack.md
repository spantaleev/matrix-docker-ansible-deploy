# Setting up MX Puppet Slack bridging (optional)

**Note**: bridging to [Slack](https://slack.com) can also happen via the
[matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) and [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) bridges supported by the playbook.

The playbook can install and configure [Beeper](https://www.beeper.com/)-maintained fork of [mx-puppet-slack](https://gitlab.com/beeper/mx-puppet-monorepo) for you.

See the project page to learn what it does and why it might be useful to you.

## Prerequisite

Follow the [OAuth credentials](https://github.com/Sorunome/mx-puppet-slack#option-2-oauth) instructions to create a new Slack app, setting the redirect URL to `https://matrix.example.com/slack/oauth`.

## Adjusting the playbook configuration

To enable the [Slack](https://slack.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mx_puppet_slack_enabled: true
# Client ID must be quoted so YAML does not parse it as a float.
matrix_mx_puppet_slack_oauth_client_id: "<SLACK_APP_CLIENT_ID>"
matrix_mx_puppet_slack_oauth_client_secret: "<SLACK_APP_CLIENT_SECRET>"
```

## Installing

After configuring the playbook, run the [installation](installing.md) command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

## Usage

Once the bot is enabled you need to start a chat with `Slack Puppet Bridge` with the handle `@_slackpuppet_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token. See mx-puppet-slack [documentation](https://github.com/Sorunome/mx-puppet-slack) for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the bridged room.

Also send `help` to the bot to see the commands available.
