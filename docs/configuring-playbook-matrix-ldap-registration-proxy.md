# Setting up matrix-ldap-registration-proxy (optional)

The playbook can install and configure [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) for you.

This proxy handles Matrix registration requests and forwards them to LDAP.

**Note**: This does support the full Matrix specification for registrations. It only provide a very coarse implementation of a basic password registration.

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_ldap_registration_proxy_enabled: true
# LDAP credentials
matrix_ldap_registration_proxy_ldap_uri: <URI>
matrix_ldap_registration_proxy_ldap_base_dn: <DN>
matrix_ldap_registration_proxy_ldap_user: <USER>
matrix_ldap_registration_proxy_ldap_password: <password>
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

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
