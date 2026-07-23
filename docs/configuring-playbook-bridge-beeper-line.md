<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Beeper LINE bridging (optional)

<sup>Refer to the common guide for configuring mautrix bridges: [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md)</sup>

The playbook can install and configure [beeper-line](https://github.com/beeper/line) for you, for bridging to [LINE](https://line.me/).

See the project's [documentation](https://github.com/beeper/line/blob/main/README.md) to learn what it does and which features it supports.

## Prerequisites

### Prepare your LINE account

The bridge logs in with the email address configured in your LINE account. If your account does not have an email address, set one in the LINE mobile app under **Settings** → **Account** → **Email address** before trying to log in.

The bridge identifies itself to LINE as a Chrome Extension client. LINE only permits one active Chrome Extension session, so the bridge and the real LINE Chrome Extension cannot be used at the same time. Logging in with either one invalidates the other session.

### Enable Appservice Double Puppet (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the common mautrix bridge guide for details.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bridge_beeper_line_enabled: true
```

### Using another container image

The playbook uses `docker.io/crispyduck/beeper-line` by default. To use an image that you have built and published elsewhere, override the complete image name:

```yaml
matrix_bridge_beeper_line_container_image_self_build: false
matrix_bridge_beeper_line_container_image: docker.io/example/beeper-line:latest
```

The role can also build the bridge directly from a Git repository on the Matrix server:

```yaml
matrix_bridge_beeper_line_container_image_self_build: true
matrix_bridge_beeper_line_container_image_self_build_repo: https://github.com/beeper/line.git
matrix_bridge_beeper_line_container_image_self_build_branch: main
```

Self-building requires more time and resources on the server than pulling a prebuilt image.

### Extending the configuration

There are additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the common mautrix bridge guide for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), and the [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional).

When following the common guide, replace `_mautrix_SERVICENAME_` in variable names with `_beeper_line_`.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`.

`just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, run `just setup-all` so those components are uninstalled.

## Usage

To use the bridge, start a chat with `@linebot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login` and follow the prompts to enter your LINE email address and password and approve the new session in the LINE mobile app.

## Troubleshooting

As with all other services, you can find the logs in systemd-journald by logging in to the server with SSH and running:

```sh
journalctl -fu matrix-beeper-line
```

### Increase logging verbosity

The default logging level for this component is `warn`. To increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug, trace
matrix_bridge_beeper_line_logging_level: debug
```
