<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Johan Swetzén
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Messenger bridging via Mautrix Meta (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge for you.

See the project's [documentation](https://docs.mau.fi/bridges/go/meta/index.html) to learn what it does and why it might be useful to you.

Since this bridge component can bridge to both [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) and you may wish to do both at the same time, the playbook makes it available via 2 different Ansible roles (`matrix-bridge-mautrix-meta-messenger` and `matrix-bridge-mautrix-meta-instagram`). The latter is a reconfigured copy of the first one (created by `just rebuild-mautrix-meta-instagram` and `bin/rebuild-mautrix-meta-instagram.sh`).

This documentation page only deals with the bridge's ability to bridge to Facebook Messenger. For bridging to Instagram, see [Setting up Instagram bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-instagram.md).

## Prerequisites

### Migrating from the old mautrix-facebook bridge

If you've been using the [mautrix-facebook](./configuring-playbook-bridge-mautrix-facebook.md) bridge, it's possible to migrate the database using [instructions from the bridge documentation](https://docs.mau.fi/bridges/go/meta/facebook-migration.html) (advanced).

Then you may wish to get rid of the Facebook bridge. To do so, send a `clean-rooms` command to the management room with the old bridge bot (`@facebookbot:example.com`). It gives you a list of portals and groups of portals you may purge. Proceed with sending commands like `clean recommended`, etc.

Then, consider disabling the old bridge in your configuration, so it won't recreate the portals when you receive new messages.

**Note**: the user ID of the new bridge bot is `@messengerbot:example.com`, not `@facebookbot:example.com`. After disabling the old bridge, its bot user will stop responding to a command.

### Enable Appservice Double Puppet (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_meta_messenger_enabled: true
```

Before proceeding to [re-running the playbook](./installing.md), you may wish to adjust the configuration further. See below.

### Bridge mode

As mentioned above, the [mautrix-meta](https://github.com/mautrix/meta) bridge supports multiple modes of operation.

The bridge can pull your Messenger messages via 3 different methods:

- (`facebook`) Facebook via `facebook.com`
- (`facebook-tor`) Facebook via `facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion` ([Tor](https://www.torproject.org/)) — does not currently proxy media downloads
- (default) (`messenger`) Messenger via `messenger.com` — usable even without a Facebook account

You may switch the mode via the `matrix_mautrix_meta_messenger_meta_mode` variable. The playbook defaults to the `messenger` mode, because it's most universal (every Facebook user has a Messenger account, but the opposite is not true).

Note that switching the mode (especially between `facebook*` and `messenger`) will intentionally make the bridge use another database (`matrix_mautrix_meta_facebook` or `matrix_mautrix_meta_messenger`) to isolate the 2 instances. Switching between Tor and non-Tor may be possible without dataloss, but your mileage may vary. Before switching to a new mode, you may wish to de-configure the old one (send `help` to the bridge bot and unbridge your portals, etc.).

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

To use the bridge, you need to start a chat with `@messengerbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain). Note that the user ID of the bridge's bot is not `@facebookbot:example.com`.

You can then follow instructions on the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/go/meta/authentication.html).

After logging in, the bridge will sync recent chats.

**Note**: given that the bot is configured in `messenger` [bridge mode](#bridge-mode) by default, you will need to log in to [messenger.com](https://messenger.com/) (not `facebook.com`!) and obtain the cookies from there.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-mautrix-meta-messenger`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# This bridge uses zerolog, so valid levels are: panic, fatal, error, warn, info, debug, trace
matrix_mautrix_meta_messenger_logging_min_level: debug
```
