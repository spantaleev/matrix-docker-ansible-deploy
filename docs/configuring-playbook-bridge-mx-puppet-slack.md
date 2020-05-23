# Setting up MX Puppet Slack (optional)

The playbook can install and configure
[mx-puppet-slack](https://github.com/Sorunome/mx-puppet-slack) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Slack](https://slack.com/) bridge just use the following
playbook configuration:


```yaml
matrix_mx_puppet_slack_enabled: true
matrix_mx_puppet_slack_client_id: ""
matrix_mx_puppet_slack_client_secret: ""
```


## Usage

Once the bot is enabled you need to start a chat with `Slack Puppet Bridge` with
the handle `@_slackpuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

Three authentication methods are available, Legacy Token, OAuth and xoxc token.
See mx-puppet-slack [documentation](https://github.com/Sorunome/mx-puppet-slack)
for more information about how to configure the bridge.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
