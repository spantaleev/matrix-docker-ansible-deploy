<!--
SPDX-FileCopyrightText: 2022 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 - 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Sable (optional)

The playbook can install and configure the [Sable](https://github.com/7w1/sable) Matrix web client for you.

Sable is a web client focusing primarily on simple, elegant and secure interface. It can be installed alongside or instead of [Element Web](./configuring-playbook-client-element-web.md), [Cinny](./configuring-playbook-client-cinny.md) and others.

## Adjusting DNS records

By default, this playbook installs Sable on the `sable.` subdomain (`sable.example.com`) and requires you to create a CNAME record for `sable`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Sable, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
sable_enabled: true
```

### Adjusting the Sable URL (optional)

By tweaking the `sable_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to a different domain (`app.example.com`) than the default one (`sable.example.com`)
sable_hostname: "app.{{ matrix_domain }}"

# Expose under the /sable subpath
# sable_path_prefix: /sable
```

After changing the domain, **you may need to adjust your DNS** records to point the Sable domain to the Matrix server.

**Note**: while there is a `sable_path_prefix` variable for changing the path where Sable is served, overriding it is [not possible](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3701), because Sable requires an application rebuild (with a tweaked build config) to be functional under a custom path. You'd need to serve Sable at a dedicated subdomain.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/galaxy/sable/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/galaxy/sable/templates/config.json.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `sable_configuration_extension_json` variable

## Installing

After configuring the playbook and [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-sable`.
