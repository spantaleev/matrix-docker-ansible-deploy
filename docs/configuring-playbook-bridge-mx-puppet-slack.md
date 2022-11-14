# Setting up MX Puppet Slack (optional)

**Note**: bridging to [Slack](https://slack.com) can also happen via the
[matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md)
bridge supported by the playbook.

The playbook can install and configure [Beeper](https://www.beeper.com/)-maintained fork of
[mx-puppet-slack](https://gitlab.com/beeper/mx-puppet-monorepo) for you.

See the project page to learn what it does and why it might be useful to you.

## Setup

To enable the [Slack](https://slack.com/) bridge:

1. Follow the
   [OAuth credentials](https://github.com/Sorunome/mx-puppet-slack#option-2-oauth)
   instructions to create a new Slack app, setting the redirect URL to
   `https://matrix.YOUR_DOMAIN/slack/oauth`.
2. Update your `vars.yml` with the following:
    ```yaml
    matrix_mx_puppet_slack_enabled: true
    # Client ID must be quoted so YAML does not parse it as a float.
    matrix_mx_puppet_slack_oauth_client_id: "<SLACK_APP_CLIENT_ID>"
    matrix_mx_puppet_slack_oauth_client_secret: "<SLACK_APP_CLIENT_SECRET>"
    ```
3. Run playbooks with `setup-all` and `start` tags:
    ```
    ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
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
