<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Toni Spets
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up a Zulip bridge (optional)

The playbook can install and configure [MatrixZulipBridge](https://github.com/GearKite/MatrixZulipBridge) for you.

See the project's [documentation](https://github.com/GearKite/MatrixZulipBridge/blob/main/README.md) to learn what it does and why it might be useful to you.

## Adjusting DNS records (optional)

By default, this playbook installs the Zulip bridge on the `matrix.` subdomain, at the `/zulip` path (https://matrix.example.com/zulip). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-zulip-bridge-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable the Zulip bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_zulip_bridge_enabled: true

# Uncomment to add one or more admins to this bridge:
#
# matrix_zulip_bridge_owner:
#  - '@yourAdminAccount:{{ matrix_domain }}'
#
# … unless you've made yourself an admin of all bots/bridges like this:
#
# matrix_admin: '@yourAdminAccount:{{ matrix_domain }}'
```

### Adjusting the Zulip bridge URL (optional)

By tweaking the `matrix_zulip_bridge_hostname` and `matrix_zulip_bridge_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_zulip_bridge_hostname: zulip.example.com
matrix_zulip_bridge_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Zulip bridge domain (`zulip.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-zulip/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@zulipbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain). If the bridge ignores you and a DM is not accepted then the owner setting may be wrong.

If you encounter issues or feel lost you can join the project room at [#matrixzulipbridge:shema.lv](https://matrix.to/#/#matrixzulipbridge:shema.lv) for help.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bridge-zulip`.
