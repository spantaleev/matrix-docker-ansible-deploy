<!--
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Dendrite (optional)

The playbook can install and configure the [Dendrite](https://github.com/element-hq/dendrite) Matrix server for you.

See the project's [documentation](https://element-hq.github.io/dendrite/) to learn what it does and why it might be useful to you.

By default, the playbook installs [Synapse](https://github.com/element-hq/synapse) as it's the only full-featured Matrix server at the moment. If that's okay, you can skip this document.

> [!WARNING]
> - **You can't switch an existing Matrix server's implementation** (e.g. Synapse -> Dendrite). Proceed below only if you're OK with losing data or you're dealing with a server on a new domain name, which hasn't participated in the Matrix federation yet.
> - **Homeserver implementations other than Synapse may not be fully functional**. The playbook may also not assist you in an optimal way (like it does with Synapse). Make yourself familiar with the downsides before proceeding

## Adjusting the playbook configuration

To use Dendrite, you **generally** need to adjust the `matrix_homeserver_implementation: synapse` configuration on your `inventory/host_vars/matrix.example.com/vars.yml` file as below:

```yaml
matrix_homeserver_implementation: dendrite
```

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-dendrite/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-dendrite/templates/dendrite.yaml.j2` for the server's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_dendrite_configuration_extension_yaml` variable

For example, to override some Dendrite settings, add the following configuration to your `vars.yml` file:

```yaml
matrix_dendrite_configuration_extension_yaml: |
  # Your custom YAML configuration for Dendrite goes here.
  # This configuration extends the default starting configuration (`matrix_dendrite_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_dendrite_configuration_yaml`.
  #
  # Example configuration extension follows:
  #
  server_notices:
    system_mxid_localpart: notices
    system_mxid_display_name: "Server Notices"
    system_mxid_avatar_url: "mxc://example.com/oumMVlgDnLYFaPVkExemNVVZ"
    room_name: "Server Notices"
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-dendrite`.

### Increase logging verbosity

The default logging level for this component is `warning`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_dendrite_configuration_extension_yaml: |
  logging:
  - type: std
    level: debug
```
