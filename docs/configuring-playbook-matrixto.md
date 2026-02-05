<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Matrix.to (optional)

The playbook can install and configure the [Matrix.to](https://github.com/matrix-org/matrix.to) URL redirection service for you.

See the project's [documentation](https://github.com/matrix-org/matrix.to/blob/main/README.md) to learn what it does and why it might be useful to you.

## Adjusting DNS records

By default, this playbook installs Matrix.to on the `mt.` subdomain (`mt.example.com`) and requires you to create a CNAME record for `mt`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Matrix.to, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_matrixto_enabled: true
```

### Adjusting the Matrix.to URL (optional)

By tweaking the `matrix_matrixto_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname
matrix_matrixto_hostname: t.example.com
```

After changing the domain, **you may need to adjust your DNS** records to point the Matrix.to domain to the Matrix server.

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-matrixto/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

Refer to the project's [documentation](https://github.com/matrix-org/matrix.to/blob/main/README.md) for available parameters, etc.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-matrixto`.
