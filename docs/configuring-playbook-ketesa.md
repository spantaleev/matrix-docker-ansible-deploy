<!--
SPDX-FileCopyrightText: 2020-2024 MDAD project contributors
SPDX-FileCopyrightText: 2020-2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2023 Christian González
SPDX-FileCopyrightText: 2024 Nikita Chernyi
SPDX-FileCopyrightText: 2024 Uğur İLTER
SPDX-FileCopyrightText: 2024-2026 Suguru Hirahara
SPDX-FileCopyrightText: 2026 Nikita Chernyi

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Ketesa (optional)

The playbook can install and configure [Ketesa](https://github.com/etkecc/ketesa) for you.

Ketesa is a fully-featured admin interface for Matrix homeservers — manage users, rooms, media, sessions, and more from one clean, responsive web UI. It is the evolution of [Awesome-Technologies/synapse-admin](https://github.com/Awesome-Technologies/synapse-admin): what began as a fork has grown into its own independent project with a redesigned interface, comprehensive Synapse and MAS API coverage, and multi-language support. See the [Ketesa v1.0.0 announcement](https://etke.cc/blog/introducing-ketesa/) for a full overview of what's new.

>[!NOTE]
>
> - Ketesa does not work with other homeserver implementations than Synapse due to API's incompatibility.
> - The latest version of Ketesa is hosted by [etke.cc](https://etke.cc/) at [admin.etke.cc](https://admin.etke.cc/). If you only need this service occasionally and trust giving your admin credentials to a 3rd party Single Page Application, you can consider using it from there and avoiding the (small) overhead of self-hosting.
> - This playbook also supports an alternative management UI in the shape of [Element Admin](./configuring-playbook-element-admin.md). Please note that it's currently less feature-rich than Ketesa and requires [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md).

## Adjusting DNS records (optional)

By default, this playbook installs Ketesa on the `matrix.` subdomain, at the `/synapse-admin` path (https://matrix.example.com/synapse-admin) — the legacy path is kept for backward compatibility. This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-ketesa-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable Ketesa, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_ketesa_enabled: true
```

**Note**: Ketesa requires Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/index.html) to function. Access to them is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, for additional security, we normally leave them unexposed, following [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints). Because Ketesa needs these APIs to function, when installing Ketesa, the playbook **automatically** exposes the Synapse Admin API publicly for you. Depending on the homeserver implementation you're using (Synapse, Dendrite), this is equivalent to:

- for [Synapse](./configuring-playbook-synapse.md) (our default homeserver implementation): `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true`
- for [Dendrite](./configuring-playbook-dendrite.md): `matrix_dendrite_container_labels_public_client_synapse_admin_api_enabled: true`

By default, Ketesa installation will be [restricted to only work with one homeserver](https://github.com/etkecc/ketesa/blob/main/README.md#restricting-available-homeserver) — the one managed by the playbook. To adjust these restrictions, tweak the `matrix_ketesa_config_restrictBaseUrl` variable.

### Adjusting the Ketesa URL (optional)

By tweaking the `matrix_ketesa_hostname` and `matrix_ketesa_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

We recommend updating the path prefix to `/ketesa` to align with the new branding, while the default `/synapse-admin` is kept for backward compatibility:

```yaml
matrix_ketesa_path_prefix: /ketesa
```

Or to change the hostname entirely:

```yaml
# Change the default hostname and path prefix
matrix_ketesa_hostname: admin.example.com
matrix_ketesa_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the Ketesa domain (`admin.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-ketesa/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_ketesa_configuration_extension_json` variable

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

After installation, Ketesa will be accessible at: `https://matrix.example.com/synapse-admin/` (or `/ketesa/` if you updated the path prefix as recommended)

To use Ketesa, you need to have [registered at least one administrator account](registering-users.md) on your server.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-ketesa`.

If you have questions, you can join this community room and feel free to ask: [#ketesa:etke.cc](https://matrix.to/#/#ketesa:etke.cc)
