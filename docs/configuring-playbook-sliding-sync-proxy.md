<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Justin Croonenberghs
SPDX-FileCopyrightText: 2023 Kuba Orlik
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2023 Samuel Meenzen
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Fabio Bonelli
SPDX-FileCopyrightText: 2024 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the Sliding Sync proxy (optional)

**Note**: The sliding-sync proxy is **not required** anymore as it's been replaced with a different method (called Simplified Sliding Sync) which is integrated into newer homeservers by default (**Conduit** homeserver from version `0.6.0` or **Synapse** from version `1.114`). This component and documentation remain here for historical purposes, but **installing this old sliding-sync proxy is generally not recommended anymore**.

The playbook can install and configure [sliding-sync](https://github.com/matrix-org/sliding-sync) proxy for you.

Sliding Sync is an implementation of [MSC3575](https://github.com/matrix-org/matrix-spec-proposals/blob/kegan/sync-v3/proposals/3575-sync.md) and a prerequisite for running Element X clients ([Element X iOS](https://github.com/element-hq/element-x-ios) and [Element X Android](https://github.com/element-hq/element-x-android)). See the project's [documentation](https://github.com/matrix-org/sliding-sync) to learn more.

## Adjusting DNS records (optional)

By default, this playbook installs the Sliding Sync proxy on the `matrix.` subdomain, at the `/sliding-sync` path (https://matrix.example.com/sliding-sync). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-sliding-sync-proxy-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Sliding Sync proxy, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_sliding_sync_enabled: true
```

### Adjusting the Sliding Sync proxy URL (optional)

By tweaking the `matrix_sliding_sync_hostname` and `matrix_sliding_sync_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_sliding_sync_hostname: ss.example.com
matrix_sliding_sync_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Sliding Sync proxy domain (`ss.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-sliding-sync/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

### External databases

Please note that, if your setup utilizes an external database, you must also establish configuration for the sliding sync proxy. Alter the defaults below to suit your configuration:

```yaml
matrix_sliding_sync_database_username: 'matrix_sliding_sync'
matrix_sliding_sync_database_password: ''
matrix_sliding_sync_database_hostname: ''
matrix_sliding_sync_database_port: 5432
matrix_sliding_sync_database_name: 'matrix_sliding_sync'
```

## Usage

You **don't need to do anything special** to make use of the Sliding Sync proxy. Simply open your client which supports Sliding Sync (like Element X) and log in.

When the Sliding Sync proxy is [installed](#installing), your `/.well-known/matrix/client` file is also updated. A new `org.matrix.msc3575.proxy` section and `url` property are added there and made to point to your Sliding Sync proxy's base URL (e.g. `https://matrix.example.com/sliding-sync`).

This allows clients which support Sliding Sync to detect the Sliding Sync proxy's URL and make use of it.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-sliding-sync`.
