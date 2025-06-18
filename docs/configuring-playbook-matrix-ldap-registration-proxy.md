<!--
SPDX-FileCopyrightText: 2022 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up matrix-ldap-registration-proxy (optional)

The playbook can install and configure [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) for you.

This proxy handles Matrix registration requests and forwards them to LDAP.

See the project's [documentation](https://gitlab.com/activism.international/matrix_ldap_registration_proxy/-/blob/main/README.md) to learn what it does and why it might be useful to you.

**Note**: This does support the full Matrix specification for registrations. It only provide a very coarse implementation of a basic password registration.

## Adjusting the playbook configuration

To enable the component, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_ldap_registration_proxy_enabled: true

# LDAP credentials
matrix_ldap_registration_proxy_ldap_uri: YOUR_URI_HERE
matrix_ldap_registration_proxy_ldap_base_dn: YOUR_DN_HERE
matrix_ldap_registration_proxy_ldap_user: YOUR_USER_HERE
matrix_ldap_registration_proxy_ldap_password: YOUR_PASSWORD_HERE
```

If you already use the [synapse external password provider via LDAP](configuring-playbook-ldap-auth.md) (that is, you have `matrix_synapse_ext_password_provider_ldap_enabled: true` and other options in your configuration) you can use the following values as configuration:

```yaml
# Use the LDAP values specified for the synapse role to setup LDAP proxy
matrix_ldap_registration_proxy_ldap_uri: "{{ matrix_synapse_ext_password_provider_ldap_uri }}"
matrix_ldap_registration_proxy_ldap_base_dn: "{{ matrix_synapse_ext_password_provider_ldap_base }}"
matrix_ldap_registration_proxy_ldap_user: "{{ matrix_synapse_ext_password_provider_ldap_bind_dn }}"
matrix_ldap_registration_proxy_ldap_password: "{{ matrix_synapse_ext_password_provider_ldap_bind_password }}"

matrix_ldap_registration_proxy_systemd_wanted_services_list_custom:
  - matrix-synapse.service
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-ldap-registration-proxy/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-ldap-registration-proxy`.
