<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Double Puppet (optional)

The playbook can install and configure the Appservice Double Puppet service for you. It is a homeserver appservice through which bridges (and potentially other services) can impersonate any user on the homeserver.

This is useful for performing [double-puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) via the appservice method. The service is an implementation of this approach.

Previously, bridges supported performing double-puppeting with the help of the [Shared Secret Auth password provider module](./configuring-playbook-shared-secret-auth.md), but this old and hacky solution has been superseded by this Appservice Double Puppet method.

## Adjusting the playbook configuration

To enable the Appservice Double Puppet service, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_double_puppet_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the service.

Take a look at:

- `roles/custom/matrix-appservice-double-puppet/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_double_puppet_registration_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Installing the service will automatically enable double puppeting for all bridges that support double puppeting via the appservice method.
