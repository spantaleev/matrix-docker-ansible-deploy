# Setting up Mautrix Hangouts bridging (optional, deprecated)

**Note**: This bridge has been deprecated in favor of [Google Chat bridge](https://github.com/mautrix/googlechat), which can be installed using [this playbook](configuring-playbook-bridge-mautrix-googlechat.md). Consider using that bridge instead of this one.

The playbook can install and configure [mautrix-hangouts](https://github.com/mautrix/hangouts) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/hangouts/index.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the [Google Hangouts](https://hangouts.google.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_hangouts_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once the bot is enabled you need to start a chat with `Hangouts bridge bot` with handle `@hangoutsbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login` to the bridge bot to receive a link to the portal from which you can enable the bridging. Open the link sent by the bot and follow the instructions.

Automatic login may not work. If it does not, reload the page and select the "Manual login" checkbox before starting. Manual login involves logging into your Google account normally and then manually getting the OAuth token from browser cookies with developer tools.

Once logged in, recent chats should show up as new conversations automatically. Other chats will get portals as you receive messages.

You can learn more about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/hangouts/authentication.html).

### Set up Double Puppeting

After successfully enabling bridging, you may wish to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do).

To set it up, you have 2 ways of going about it.

#### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

#### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Hangouts` device some time in the future, as that would break the Double Puppeting feature
