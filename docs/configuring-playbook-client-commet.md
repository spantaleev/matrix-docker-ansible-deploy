<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Commet (optional)

The playbook can install and configure the [Commet](https://github.com/commetchat/commet) Matrix web client for you.

## Adjusting DNS records

By default, this playbook installs Commet on the `commet.` subdomain (`commet.example.com`) and requires you to create a CNAME record for `commet`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Commet, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_commet_enabled: true
```

### Adjusting the Commet URL (optional)

By tweaking the `matrix_client_commet_hostname` and `matrix_client_commet_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Commet.
matrix_client_commet_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /commet subpath
matrix_client_commet_path_prefix: /commet
```

After changing the domain, **you may need to adjust your DNS** records to point the Commet domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

**Note**: `matrix_client_commet_path_prefix` must either be `/` or not end with a slash (e.g. `/commet`).

### Adjusting the default homeserver (optional)

Commet is configured with a `default_homeserver` value. By default, the playbook uses `matrix.org`.

To change it, add the following configuration to your `vars.yml` file:

```yaml
matrix_client_commet_default_homeserver: "{{ matrix_domain }}"
```

### Adjusting the Commet version/branch to build (optional)

When self-building the container image (`matrix_client_commet_container_image_self_build: true`), the playbook checks out the Commet source repository and builds an image from it.

To build from a different git branch/tag/SHA, set `matrix_client_commet_version` in your `vars.yml` file:

```yaml
# Examples: "main", "v1.2.3", "feature-branch", "a1b2c3d4"
matrix_client_commet_version: "main"
```

**Note**: by default, the image tag is derived from `matrix_client_commet_version` (`localhost/matrix-client-commet:{{ matrix_client_commet_version }}`). If your branch name contains `/` (e.g. `feature/foo`), override `matrix_client_commet_container_image` (and optionally `matrix_client_commet_container_image_self_build_version_tag`) to a Docker-tag-safe value.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-client-commet/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-client-commet/templates/global_config.json.j2` for the component's default runtime configuration

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-commet`.
