<!--
SPDX-FileCopyrightText: 2025 Nikita Chernyi
SPDX-FileCopyrightText: 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up FluffyChat Web (optional)

The playbook can install and configure the [FluffyChat Web](https://github.com/krille-chan/fluffychat) Matrix client for you.

FluffyChat Web is a cute cross-platform (web, iOS, Android) messenger for Matrix written in [Flutter](https://flutter.dev/).

💡 **Note**: the latest version of FluffyChat Web is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Application, you can consider using it from there:

- [fluffychat.im](https://fluffychat.im/web), hosted by the [FluffyChat](https://fluffy.chat/) developers

## Adjusting DNS records

By default, this playbook installs FluffyChat Web on the `fluffychat.` subdomain (`fluffychat.example.com`) and requires you to create a CNAME record for `fluffychat`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable FluffyChat Web, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_fluffychat_enabled: true
```

### Adjusting the FluffyChat Web URL (optional)

By tweaking the `matrix_client_fluffychat_hostname` and `matrix_client_fluffychat_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for FluffyChat Web.
matrix_client_fluffychat_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /fluffychat subpath
matrix_client_fluffychat_path_prefix: /fluffychat
```

After changing the domain, **you may need to adjust your DNS** records to point the FluffyChat Web domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-fluffychat`.
