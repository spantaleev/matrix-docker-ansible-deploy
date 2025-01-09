# Setting up Mautrix Hangouts bridging (optional, deprecated)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

💡 **Note**: This bridge has been deprecated in favor of [Google Chat bridge](https://github.com/mautrix/googlechat), which can be installed using [this playbook](configuring-playbook-bridge-mautrix-googlechat.md). Installing the mautrix-hangouts bridge is **no longer possible**. For now, this documentation page remains here for historical purposes.

The playbook can install and configure [mautrix-hangouts](https://github.com/mautrix/hangouts) for you.

## Prerequisite (optional)

### Enable Shared Secret Auth

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the [Google Hangouts](https://hangouts.google.com/) bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_hangouts_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#setting-the-bot-s-username-optional), etc.

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

To use the bridge, you need to start a chat with `Hangouts bridge bot` with handle `@hangoutsbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You then need to send `login` to the bridge bot to receive a link to the portal from which you can enable the bridging. Open the link sent by the bot and follow the instructions.

Automatic login may not work. If it does not, reload the page and select the "Manual login" checkbox before starting. Manual login involves logging into your Google account normally and then manually getting the OAuth token from browser cookies with developer tools.

Once logged in, recent chats should show up as new conversations automatically. Other chats will get portals as you receive messages.
