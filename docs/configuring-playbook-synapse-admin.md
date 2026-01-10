<!--
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2023 Christian González
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Uğur İLTER

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Synapse Admin (optional)

The playbook can install and configure [etkecc/synapse-admin](https://github.com/etkecc/synapse-admin) (a [feature-rich](https://github.com/etkecc/synapse-admin#fork-differences) fork of [Awesome-Technologies/synapse-admin](https://github.com/Awesome-Technologies/synapse-admin), community room: [#synapse-admin:etke.cc](https://matrix.to/#/#synapse-admin:etke.cc)) for you.

synapse-admin is a web UI tool you can use to **administrate users, rooms, media, etc. on your Matrix server**. It's designed to work with the Synapse homeserver implementation and WON'T work with Dendrite because [Dendrite Admin API](https://element-hq.github.io/dendrite/administration/adminapi) differs from [Synapse Admin API](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/).

💡 **Note**: the latest version of synapse-admin is hosted by [etke.cc](https://etke.cc/) at [admin.etke.cc](https://admin.etke.cc/). If you only need this service occasionally and trust giving your admin credentials to a 3rd party Single Page Application, you can consider using it from there and avoiding the (small) overhead of self-hosting.

💡 **Note**: The playbook also supports an alternative management UI in the shape of [Element Admin](./configuring-playbook-element-admin.md). However, it's currently less feature-rich than Synapse Admin and has a dependency on [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md).

## Adjusting DNS records (optional)

By default, this playbook installs Synapse Admin on the `matrix.` subdomain, at the `/synapse-admin` path (https://matrix.example.com/synapse-admin). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-synapse-admin-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Synapse Admin, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_admin_enabled: true
```

**Note**: Synapse Admin requires Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/index.html) to function. Access to them is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, for additional security, we normally leave them unexposed, following [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints). Because Synapse Admin needs these APIs to function, when installing Synapse Admin, the playbook **automatically** exposes the Synapse Admin API publicly for you. Depending on the homeserver implementation you're using (Synapse, Dendrite), this is equivalent to:

- for [Synapse](./configuring-playbook-synapse.md) (our default homeserver implementation): `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true`
- for [Dendrite](./configuring-playbook-dendrite.md): `matrix_dendrite_container_labels_public_client_synapse_admin_api_enabled: true`

By default, synapse-admin installation will be [restricted to only work with one homeserver](https://github.com/etkecc/synapse-admin/blob/e21e44362c879ac41f47c580b04210842b6ff3d7/README.md#restricting-available-homeserver) — the one managed by the playbook. To adjust these restrictions, tweak the `matrix_synapse_admin_config_restrictBaseUrl` variable.

### Adjusting the Synapse Admin URL (optional)

By tweaking the `matrix_synapse_admin_hostname` and `matrix_synapse_admin_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_synapse_admin_hostname: admin.example.com
matrix_synapse_admin_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Synapse Admin domain (`admin.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-synapse-admin/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_synapse_admin_configuration_extension_json` variable

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

After installation, Synapse Admin will be accessible at: `https://matrix.example.com/synapse-admin/`

To use Synapse Admin, you need to have [registered at least one administrator account](registering-users.md) on your server.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-synapse-admin`.
