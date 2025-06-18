<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Toni Spets
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Heisenbridge bouncer-style IRC bridging (optional)

**Note**: bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) can also happen via the [matrix-appservice-irc](configuring-playbook-bridge-appservice-irc.md) bridge supported by the playbook.

The playbook can install and configure [Heisenbridge](https://github.com/hifi/heisenbridge) — the bouncer-style [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) bridge for you.

See the project's [documentation](https://github.com/hifi/heisenbridge/blob/master/README.md) to learn what it does and why it might be useful to you. You can also take a look at [this demonstration video](https://www.youtube.com/watch?v=nQk1Bp4tk4I).

## Adjusting DNS records (optional)

By default, this playbook installs Heisenbridge on the `matrix.` subdomain, at the `/heisenbridge` path (https://matrix.example.com/heisenbridge). It would handle media requests there (see the [release notes for Heisenbridge v1.15.0](https://github.com/hifi/heisenbridge/releases/tag/v1.15.0)). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-heisenbridge-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Heisenbridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_heisenbridge_enabled: true

# Setting the owner is optional as the first local user to DM `@heisenbridge:example.com` will be made the owner.
# If you are not using a local user you must set it as otherwise you can't DM it at all.
matrix_heisenbridge_owner: "@alice:{{ matrix_domain }}"

# Uncomment to enable identd on host port 113/TCP (optional)
# matrix_heisenbridge_identd_enabled: true
```

### Adjusting the Heisenbridge URL (optional)

By tweaking the `matrix_heisenbridge_hostname` and `matrix_heisenbridge_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_heisenbridge_hostname: heisenbridge.example.com
matrix_heisenbridge_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Heisenbridge domain (`heisenbridge.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-heisenbridge/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@heisenbridge:example.com` (where `example.com` is your base domain, not the `matrix.` domain). If the bridge ignores you and a DM is not accepted then the owner setting may be wrong.

Help is available for all commands with the `-h` switch.

You can also learn the basics by watching [this demonstration video](https://www.youtube.com/watch?v=nQk1Bp4tk4I).

If you encounter issues or feel lost you can join the project room at [#heisenbridge:vi.fi](https://matrix.to/#/#heisenbridge:vi.fi) for help.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-heisenbridge`.
