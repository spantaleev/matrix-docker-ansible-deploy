<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors
SPDX-FileCopyrightText: 2026 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Google Voice bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-gvoice](https://github.com/mautrix/gvoice) for you, for bridging to [Google Voice](https://voice.google.com/).

See the project's [documentation](https://docs.mau.fi/bridges/go/gvoice/index.html) to learn what it does and why it might be useful to you.

## Prerequisite (optional)

### Enable Appservice Double Puppet

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_gvoice_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

<!-- NOTE: relay mode is not supported for this bridge -->
See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, start a chat with `@gvoicebot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Google Voice has no phone to pair and no QR code to scan. It logs in with cookies, which you copy from a browser already signed in to [voice.google.com](https://voice.google.com/) and hand to the bot. It is fiddlier than scanning a code and feels more suspicious than it is, but Google leaves no cleaner door open. The bridge's [official Authentication guide](https://docs.mau.fi/bridges/go/gvoice/authentication.html) has the exact cookies to grab and the steps for grabbing them.

Those cookies are a login session, and Google expires them on its own schedule. When they lapse the bridge goes quiet and you log in again. Nothing is broken, that is just how cookie auth ages.

Once you log in, the bridge builds portal rooms for your recent conversations and carries text and media both ways. Don't reach for it to start a brand-new chat or to place a call, though. That ground still belongs to Google Voice, so keep the app around for those.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-gvoice`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_mautrix_gvoice_logging_level: 'debug'
```
