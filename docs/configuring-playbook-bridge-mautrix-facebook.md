<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Hugues Morisset
SPDX-FileCopyrightText: 2021 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 László Várady
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Mautrix Facebook bridging (optional, deprecated)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

**Note**: This bridge has been deprecated in favor of the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge, which can be [installed using this playbook](configuring-playbook-bridge-mautrix-meta-messenger.md). Consider using that bridge instead of this one.

The playbook can install and configure [mautrix-facebook](https://github.com/mautrix/facebook) for you.

See the project's [documentation](https://github.com/mautrix/facebook/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisite (optional)

### Enable Shared Secret Auth

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_facebook_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@facebookbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You then need to send `login YOUR_FACEBOOK_EMAIL_ADDRESS` to the bridge bot to enable bridging for your Facebook Messenger account.

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-facebook`.

### Increase logging verbosity

The default logging level for this component is `WARNING`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_mautrix_facebook_logging_level: DEBUG
```

### Facebook rejecting login attempts and forcing you to change password

If your Matrix server is in a wildly different location than where you usually use your Facebook account from, the bridge's login attempts may be outright rejected by Facebook. Along with that, Facebook may even force you to change the account's password.

If you happen to run into this problem while [setting up bridging](#usage), try to first get a successful session up by logging in to Facebook through the Matrix server's IP address.

The easiest way to do this may be to use [sshuttle](https://sshuttle.readthedocs.io/) to proxy your traffic through the Matrix server.

Example command for proxying your traffic through the Matrix server:

```sh
sshuttle -r root@matrix.example.com:22 0/0
```

Once connected, you should be able to verify that you're browsing the web through the Matrix server's IP by checking [icanhazip](https://icanhazip.com/).

Then proceed to log in to [Facebook/Messenger](https://www.facebook.com/).

Once logged in, proceed to [set up bridging](#usage).

If that doesn't work, enable 2FA (see: [Facebook help page on enabling 2FA](https://www.facebook.com/help/148233965247823)) and try to login again with a new password, and entering the 2FA code when prompted, it may take more then one try, in between attempts, check facebook.com to see if they are requiring another password change
