# Setting up Mautrix Slack bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

**Note**: bridging to [Slack](https://slack.com/) can also happen via the [mx-puppet-slack](configuring-playbook-bridge-mx-puppet-slack.md) and [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) bridges supported by the playbook.
- For using as a Bot we recommend the [Appservice Slack](configuring-playbook-bridge-appservice-slack.md), because it supports plumbing. Note that it is not available for new installation unless you have already created a classic Slack application, because the creation of classic Slack applications, which this bridge makes use of, has been discontinued.
- For personal use with a slack account we recommend the `mautrix-slack` bridge (the one being discussed here), because it is the most fully-featured and stable of the 3 Slack bridges supported by the playbook.

The playbook can install and configure [mautrix-slack](https://github.com/mautrix/slack) for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/slack/index.html) to learn what it does and why it might be useful to you.

See the [features and roadmap](https://github.com/mautrix/slack/blob/main/ROADMAP.md) for more information.

## Prerequisites

For using this bridge, you would need to authenticate by **providing your username and password** (legacy) or by using a **token login**. See more information in the [docs](https://docs.mau.fi/bridges/go/slack/authentication.html).

Note that neither of these methods are officially supported by Slack. [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) uses a Slack bot account which is the only officially supported method for bridging a Slack channel.

### Enable Appservice Double Puppet (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_slack_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#setting-the-bot-s-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

1. Start a chat with `@slackbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).
2. If you would like to login to Slack using a token, send the `login-token` command, otherwise, send the `login-password` command. Read [here](https://docs.mau.fi/bridges/go/slack/authentication.html) on how to retrieve your token and cookie token.
3. The bot should respond with "Successfully logged into <email> for team <workspace>"
4. Now that you're logged in, you can send `help` to the bot to see the available commands.
5. Slack channels should automatically begin bridging if you authenticated using a token. Otherwise, you must wait to receive a message in the channel if you used password authentication.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/go/slack/authentication.html).
