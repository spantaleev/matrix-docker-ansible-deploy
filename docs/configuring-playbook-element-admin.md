<!--
SPDX-FileCopyrightText: 2024 wjbeckett
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Element Admin (optional)

The playbook can install and configure [Element Admin](https://github.com/element-hq/element-admin) for you.

Element Admin is a web-based administration panel for Synapse and [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md).

See the project's [documentation](https://github.com/element-hq/element-admin) to learn more.

💡 **Note**: This project is still very young and doesn't have many features. For now, it's recommended to use [Synapse Admin](./configuring-playbook-synapse-admin.md) instead. Deployments that use [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md) can use Element Admin for user-management (something that Synapse Admin can't do), while continuing to use Synapse Admin for all other purposes.

## Prerequisites

- A [Synapse](configuring-playbook-synapse.md) homeserver with its Admin API enabled (the playbook automatically enables it for you when you enable Element Admin)
- [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md) with its Admin API enabled (the playbook automatically enables it for you when you enable Element Admin)

## Decide on a domain and path

By default, the Element Admin is configured to be served on the `admin.element.example.com` domain.

If you'd like to run Element Admin on another hostname, see the [Adjusting the Element Admin URL](#adjusting-the-element-admin-url-optional) section below.

## Adjusting DNS records (optional)

By default, this playbook installs Element Admin on the `admin.element.` subdomain (`admin.element.example.com`) and requires you to create a `CNAME` record for `admin.element`, which targets `matrix.example.com`.

When setting these values, replace `example.com` with your own.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_element_admin_enabled: true
```

### Adjusting the Element Admin URL (optional)

By tweaking the `matrix_element_admin_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
matrix_element_admin_hostname: element-admin.example.com
```

> [!WARNING]
> A `matrix_element_admin_path_prefix` variable is also available and mean to let you configure a path prefix for the Element Admin service, but **Element Admin does not support running under a sub-path yet**.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
