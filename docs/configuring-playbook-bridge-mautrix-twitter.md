# Setting up Mautrix Twitter (optional)

**Note**: bridging to [Twitter](https://twitter.com/) can also happen via the [mx-puppet-twitter](configuring-playbook-bridge-mx-puppet-twitter.md) bridge supported by the playbook.

The playbook can install and configure [mautrix-twitter](https://github.com/mautrix/twitter) for you.

See the project's [documentation](https://github.com/mautrix/twitter) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_mautrix_twitter_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Appservice Double Puppet or Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service or the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

Enabling double puppeting by enabling the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service works at the time of writing, but is deprecated and will stop working in the future.

### Method 2: manually, by asking each user to provide a working access token

This method is currently not available for the Mautrix-Twitter bridge, but is on the [roadmap](https://github.com/mautrix/twitter/blob/master/ROADMAP.md) under Misc/Manual login with `login-matrix`

## Usage

1. You then need to start a chat with `@twitterbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
2. Send login-cookie to start the login. The bot should respond with instructions on how to proceed.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/twitter/authentication.html).

After successfully enabling bridging, you may wish to [set up Double Puppeting](#set-up-double-puppeting), if you haven't already done so.
