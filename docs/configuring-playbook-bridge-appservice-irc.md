<!--
SPDX-FileCopyrightText: 2019 - 2021 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 MDAD project contributors
SPDX-FileCopyrightText: 2020 Lee Verberne
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice IRC bridging (optional)

**Note**: bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) can also happen via the [Heisenbridge](configuring-playbook-bridge-heisenbridge.md) bridge supported by the playbook.

The playbook can install and configure the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge for you.

See the project's [documentation](https://github.com/matrix-org/matrix-appservice-irc/blob/master/HOWTO.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_irc_enabled: true

matrix_appservice_irc_ircService_servers:
  irc.example.com:
    name: "ExampleNet"
    port: 6697
    ssl: true
    sasl: false
    allowExpiredCerts: false
    sendConnectionMessages: true
    botConfig:
      enabled: true
      nick: "MatrixBot"
      joinChannelsIfNoUsers: true
    privateMessages:
      enabled: true
      federate: true
    dynamicChannels:
      enabled: true
      createAlias: true
      published: true
      joinRule: public
      groupId: +myircnetwork:localhost
      federate: true
      aliasTemplate: "#irc_$CHANNEL"
    membershipLists:
      enabled: false
      floodDelayMs: 10000
      global:
        ircToMatrix:
          initial: false
          incremental: false
        matrixToIrc:
          initial: false
          incremental: false
    matrixClients:
      userTemplate: "@irc_$NICK"
      displayName: "$NICK (IRC)"
      joinAttempts: -1
    ircClients:
      nickTemplate: "$DISPLAY[m]"
      allowNickChanges: true
      maxClients: 30
      idleTimeout: 10800
      reconnectIntervalMs: 5000
      concurrentReconnectLimit: 50
      lineLimit: 3
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-appservice-irc/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-appservice-irc/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_irc_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@irc_bot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-appservice-irc`.

### Configuring for logging

The default logging level for this component is `debug`, and the log is output to the console only. If you want to change the verbosity or enable logging to a file, add the following configuration to your `vars.yml` file (adapt to your needs) and re-run the playbook:

```yaml
matrix_appservice_irc_configuration_extension_yaml: |
  logging:
    # Level to log on console/logfile.
    # Valid values: error, warn, info, debug
    level: "debug"
    # The file location to log to. This is relative to the project directory.
    logfile: "debug.log"
    # The file location to log errors to. This is relative to the project directory.
    errfile: "errors.log"
```
