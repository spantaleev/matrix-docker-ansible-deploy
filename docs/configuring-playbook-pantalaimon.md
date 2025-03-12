<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Pantalaimon (E2EE aware proxy daemon) (optional)

The playbook can install and configure the [pantalaimon](https://github.com/matrix-org/pantalaimon) E2EE aware proxy daemon for you.

See the project's [documentation](https://github.com/matrix-org/pantalaimon/blob/master/README.md) to learn what it does and why it might be useful to you.

This role exposes Pantalaimon's API only within the container network, so bots and clients installed on the same machine can use it. In particular the [Draupnir](configuring-playbook-bot-draupnir.md) and [Mjolnir](configuring-playbook-bot-mjolnir.md) roles (and possibly others) can use it.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_pantalaimon_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-pantalaimon/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_pantalaimon_configuration` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-pantalaimon`.

The default logging level for this component is `Warning`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: Error, Warning, Info, Debug
matrix_pantalaimon_log_level: Debug
```
