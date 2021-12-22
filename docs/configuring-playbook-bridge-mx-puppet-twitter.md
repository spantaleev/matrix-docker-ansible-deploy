# Setting up MX Puppet Twitter (optional)

**Note**: bridging to [Twitter](https://twitter.com/) can also happen via the [mautrix-twitter](configuring-playbook-bridge-mautrix-twitter.md) bridge supported by the playbook.

The playbook can install and configure
[mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) for you.

See the project page to learn what it does and why it might be useful to you.

To enable the [Twitter](https://twitter.com) bridge, make an app on [developer.twitter.com](https://developer.twitter.com/en/apps)
and fill out the following playbook configuration.

```yaml
matrix_mx_puppet_twitter_enabled: true
matrix_mx_puppet_twitter_consumer_key: ''
matrix_mx_puppet_twitter_consumer_secret: ''
matrix_mx_puppet_twitter_access_token: ''
matrix_mx_puppet_twitter_access_token_secret: ''
matrix_mx_puppet_twitter_environment: ''
```


## Usage

Once the bot is enabled you need to start a chat with `Twitter Puppet Bridge` with
the handle `@_twitterpuppet_bot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base
domain, not the `matrix.` domain).

To log in, use `link` and click the link.

Once logged in, send `list` to the bot user to list the available rooms.

Clicking rooms in the list will result in you receiving an invitation to the
bridged room.

Also send `help` to the bot to see the commands available.
