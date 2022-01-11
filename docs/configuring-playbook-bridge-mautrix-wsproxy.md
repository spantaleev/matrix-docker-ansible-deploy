# Setting up Mautrix wsproxy (optional)

The playbook can install and configure [mautrix-wsproxy](https://github.com/mautrix/wsproxy) for you.

See the project's [documentation](https://github.com/mautrix/wsproxy#readme) to learn what it does and why it might be useful to you.

Use the following playbook configuration:

```yaml
matrix_mautrix_wsproxy_enabled: true
matrix_mautrix_wsproxy_appservice_token: 'random string'
matrix_mautrix_wsproxy_homeserver_token: 'random string'
```


## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://github.com/tulir/mautrix-hangouts/wiki/Authentication#double-puppeting) (hint: you most likely do), you have 1 way of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

## Usage

Follow the [matrix-imessage documenation](https://docs.mau.fi/bridges/go/imessage/index.html) for running `matrix-imessage` on your iOS/MacOS device.
