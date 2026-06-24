<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors
SPDX-FileCopyrightText: 2026 Jason LaGuidice

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up RustPush (iMessage) bridging (optional)

> **Note:** This bridge is in early development and may have stability issues. It may not be desirable to deploy this to a large number of users. Your testing and feedback is appreciated.

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [RustPush bridge to iMessage](https://github.com/jasonlaguidice/imessage) for you using Apple's push notification service.

See the project's [documentation](https://github.com/jasonlaguidice/imessage/blob/main/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Hardware Key Extraction

To use this bridge on Linux (Docker), each user needs a **hardware key** extracted from a real Mac. This key contains hardware identifiers needed for iMessage registration. Hardware keys can be shared by a number of users (approximately 20) before causing issues with Apple.

The key is entered interactively through the bridge bot's login flow (not configured via Ansible variables). See the upstream [README](https://github.com/jasonlaguidice/imessage/blob/main/README.md) for instructions on extracting the key.

If extracted from an Intel Mac, the Mac does not need to remain running after the key is extracted for this bridge to work. Apple Silicon Macs must run a NAC relay and thus must remain running.

### Phone Number Registration (optional)

This bridge can **not** do phone number registration (PNR). The only way to have your phone number registered and used (instead of an Apple ID e-mail address) is to have an iPhone connected to your Apple account. Reference the [BlueBubbles Phone Number Registration Guide](https://docs.bluebubbles.app/server/advanced/registering-a-phone-number-with-your-imessage-account) for information on how to set this up.

### Enable Appservice Double Puppet (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_rustpush_bridge_enabled: true
```

### Disable Backfill (optional)

Backfill can be disabled globally if desired via config. By default, the bridge will backfill from iCloud (CloudKit) and APNS if available. Backfill from `chat.db` is only possible when the bridge is running on MacOS.

```yaml
matrix_rustpush_bridge_backfill_enabled: false
```

### Extending the Configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

To use the bridge, you need to start a chat with `@rustpushbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

After logging in, the bridge will start receiving iMessages and creating portal rooms.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-rustpush-bridge`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_rustpush_bridge_logging_level: 'debug'

# Enable debug logging for RustPush
matrix_rustpush_bridge_rust_log: "warn,rustpushgo=info,openabsinthe=debug"
```
