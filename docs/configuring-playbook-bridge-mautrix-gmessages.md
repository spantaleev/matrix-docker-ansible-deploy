# Setting up Mautrix gmessages (optional)

The playbook can install and configure [mautrix-gmessages](https://github.com/mautrix/gmessages) for you, for bridging to [Google Messages](https://messages.google.com/).

See the project's [documentation](https://docs.mau.fi/bridges/go/gmessages/index.html) to learn what it does and why it might be useful to you.

Use the following playbook configuration:

```yaml
matrix_mautrix_gmessages_enabled: true
```

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-gmessages` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@gmessagesbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
