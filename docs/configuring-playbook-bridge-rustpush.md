<!--
SPDX-FileCopyrightText: 2025 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up RustPush bridging (optional)

<sup>Refer the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [mautrix-imessage with RustPush](https://github.com/lrhodin/imessage) for you, which provides a bridge to [iMessage](https://support.apple.com/messages) using Apple's push notification service (no Mac needed at runtime).

See the project's [documentation](https://github.com/lrhodin/imessage/blob/main/README.md) to learn what it does and why it might be useful to you.

**Note**: This bridge is built from source (no pre-built Docker image exists). The build process requires Rust, Go, and C toolchains, which means the initial build will take significant time and resources.

## Prerequisites

### Hardware Key Extraction

To use this bridge on Linux (Docker), you need a **hardware key** extracted from a real Mac. This key contains hardware identifiers needed for iMessage registration.

The key is entered interactively through the bridge bot's login flow (not configured via Ansible variables). See the upstream [README](https://github.com/lrhodin/imessage/blob/main/README.md) for instructions on extracting the key.

### Enable Appservice Double Puppet (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_rustpush_bridge_enabled: true
```

### Backfill (optional)

Backfill is disabled by default because Linux Docker cannot access the macOS `chat.db` file. If you are running on macOS with Full Disk Access, you can enable it:

```yaml
matrix_rustpush_bridge_backfill_enabled: true
matrix_rustpush_bridge_initial_sync_days: 365
```

### Extending the configuration

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

- The first run will take longer than usual because the Docker image is built from source (Rust + Go compilation).

## Usage

To use the bridge, you need to start a chat with `@imessagebot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

The bridge supports two login flows:

1. **External Key Login** (Linux/Docker): Enter your hardware key (base64), then Apple ID credentials and 2FA code.
2. **Apple ID Login** (macOS only): Enter Apple ID credentials and 2FA code directly.

After logging in, the bridge will start receiving iMessages and creating portal rooms.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-rustpush-bridge`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_rustpush_bridge_logging_level: 'debug'
```
