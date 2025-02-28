<!--
SPDX-FileCopyrightText: 2018 - 2022 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up the LDAP authentication password provider module (optional, advanced)

The playbook can install and configure the [matrix-synapse-ldap3](https://github.com/matrix-org/matrix-synapse-ldap3) LDAP Auth password provider for you.

See the project's [documentation](https://github.com/matrix-org/matrix-synapse-ldap3/blob/main/README.rst) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_ext_password_provider_ldap_enabled: true
matrix_synapse_ext_password_provider_ldap_uri:
  - "ldap://ldap-01.example.com:389"
  - "ldap://ldap-02.example.com:389"
matrix_synapse_ext_password_provider_ldap_start_tls: true
matrix_synapse_ext_password_provider_ldap_base: "ou=users,dc=example,dc=com"
matrix_synapse_ext_password_provider_ldap_attributes_uid: "uid"
matrix_synapse_ext_password_provider_ldap_attributes_mail: "mail"
matrix_synapse_ext_password_provider_ldap_attributes_name: "cn"
matrix_synapse_ext_password_provider_ldap_bind_dn: ""
matrix_synapse_ext_password_provider_ldap_bind_password: ""
matrix_synapse_ext_password_provider_ldap_filter: ""
```

### Authenticating only using a password provider

If you wish for users to **authenticate only against configured password providers** (like this one), **without consulting Synapse's local database**, you can disable it by adding the following configuration to your `vars.yml` file:

```yaml
matrix_synapse_password_config_localdb_enabled: false
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

### Handling user registration

If you wish for users to also be able to make new registrations against LDAP, you may **also** wish to [set up the ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md).
