# Setting up Mautrix Slack (optional)

**Note**: bridging to [Slack](https://slack.com/) can also happen via the [mx-puppet-slack](configuring-playbook-bridge-mx-puppet-slack.md) and [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) bridges supported by the playbook.
- For using as a Bot we recommend the [Appservice Slack](configuring-playbook-bridge-appservice-slack.md), because it supports plumbing.
- For personal use with a slack account we recommend the `mautrix-slack` bridge (the one being discussed here), because it is the most fully-featured and stable of the 3 Slack bridges supported by the playbook.

The playbook can install and configure [mautrix-slack](https://github.com/mautrix/slack) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/slack/index.html) to learn what it does and why it might be useful to you.

See the [features and roadmap](https://github.com/mautrix/slack/blob/main/ROADMAP.md) for more information.


## Prerequisites

For using this bridge, you would need to authenticate by **providing your username and password** (legacy) or by using a **token login**. See more information in the [docs](https://docs.mau.fi/bridges/go/slack/authentication.html).

Note that neither of these methods are officially supported by Slack. [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) uses a Slack bot account which is the only officially supported method for bridging a Slack channel.


## Installing

To enable the bridge, add this to your `vars.yml` file:

```yaml
matrix_mautrix_slack_enabled: true
```

You may optionally wish to add some [Additional configuration](#additional-configuration), or to [prepare for double-puppeting](#set-up-double-puppeting) before the initial installation.

After adjusting your `vars.yml` file, re-run the playbook and restart all services: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

To make use of the bridge, see [Usage](#usage) below.


### Additional configuration

There are some additional options you may wish to configure with the bridge.

Take a look at:

- `roles/custom/matrix-bridge-mautrix-slack/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-mautrix-slack/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_mautrix_slack_configuration_extension_yaml` variable


### Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

#### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

#### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Slack` device some time in the future, as that would break the Double Puppeting feature


## Usage

1. Start a chat with `@slackbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
2. If you would like to login to Slack using a token, send the `login-token` command, otherwise, send the `login-password` command. Read [here](https://docs.mau.fi/bridges/go/slack/authentication.html) on how to retrieve your token and cookie token.
3. The bot should respond with "Successfully logged into <email> for team <workspace>"
4. Now that you're logged in, you can send a `help` command to the bot again, to see additional commands you have access to.
5. Slack channels should automatically begin bridging if you authenticated using a token. Otherwise, you must wait to receive a message in the channel if you used password authentication.
