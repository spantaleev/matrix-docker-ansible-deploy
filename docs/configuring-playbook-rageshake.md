<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the rageshake bug report server (optional)

The playbook can install and configure the [rageshake](https://github.com/matrix-org/rageshake) bug report server for you.

See the project's [documentation](https://github.com/matrix-org/rageshake/blob/main/README.md) to learn what it does and why it might be useful to you.

**Note**: most people don't need to install rageshake to collect bug reports. This component is only useful to people who develop/build their own Matrix client applications themselves.

## Adjusting DNS records

By default, this playbook installs rageshake on the `rageshake.` subdomain (`rageshake.example.com`) and requires you to create a CNAME record for `rageshake`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable rageshake, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_rageshake_enabled: true
```

### Adjusting the rageshake URL (optional)

By tweaking the `matrix_rageshake_hostname` and `matrix_rageshake_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for rageshake.
matrix_rageshake_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /rageshake subpath
matrix_rageshake_path_prefix: /rageshake
```

After changing the domain, **you may need to adjust your DNS** records to point the rageshake domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-rageshake/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-rageshake/templates/config.yaml.j2` for the server's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_rageshake_configuration_extension_yaml` variable

```yaml
matrix_rageshake_configuration_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_rageshake_configuration_extension_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_rageshake_configuration_extension_yaml`.

  github_token: secrettoken

  github_project_mappings:
     my-app: octocat/HelloWorld
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Refer to the project's [documentation](https://github.com/matrix-org/rageshake/blob/main/README.md) for available APIs, etc.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-rageshake`.
