<!--
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up WeChat bridging (optional)

The playbook can install and configure [matrix-wechat](https://github.com/duo/matrix-wechat) for you, for bridging to [WeChat](https://www.wechat.com/).

See the project's [documentation](https://github.com/duo/matrix-wechat/blob/master/README.md) to learn what it does and why it might be useful to you.

> [!WARNING]
> This bridge does not work against newer versions of Synapse anymore. See [this issue](https://github.com/duo/matrix-wechat/issues/33). Don't even bother installing it. Unless bridge maintenance is resumed and fixes this issue, we have no choice but to remove it from the playbook.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_wechat_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-wechat/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-wechat/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_wechat_configuration_extension_yaml` variable

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

To use the bridge, you need to start a chat with `@wechatbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `help` to the bot to see the available commands.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-wechat`.

### Increase logging verbosity

The default logging level for this component is `warn`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: fatal, error, warn, info, debug
matrix_wechat_log_level: 'debug'
```
