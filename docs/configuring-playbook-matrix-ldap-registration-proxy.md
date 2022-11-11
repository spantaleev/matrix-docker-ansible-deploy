# Setting up matrix-ldap-registration-proxy (optional)

The playbook can install and configure [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) for you.

This proxy handles Matrix registration requests and forwards them to LDAP.

**Please note:** This does support the full Matrix specification for registrations. It only provide a very coarse
implementation of a basic password registration.

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_ldap_registration_proxy_enabled: true
# LDAP credentials
matrix_ldap_registration_proxy_ldap_uri: <URI>
matrix_ldap_registration_proxy_ldap_base_dn: <DN>
matrix_ldap_registration_proxy_ldap_user: <USER>
matrix_ldap_registration_proxy_ldap_password: <password>
```

If you already use the [synapse external password provider via LDAP](configuring-playbook-ldap-auth.md) (that is, you have `matrix_synapse_ext_password_provider_ldap_enabled: true` and other options in your configuration)
you can use the following values as configuration:

```yaml
# Use the LDAP values specified for the synapse role to setup LDAP proxy
matrix_ldap_registration_proxy_ldap_uri: "{{ matrix_synapse_ext_password_provider_ldap_uri }}"
matrix_ldap_registration_proxy_ldap_base_dn: "{{ matrix_synapse_ext_password_provider_ldap_base }}"
matrix_ldap_registration_proxy_ldap_user: "{{ matrix_synapse_ext_password_provider_ldap_bind_dn }}"
matrix_ldap_registration_proxy_ldap_password: "{{ matrix_synapse_ext_password_provider_ldap_bind_password }}"
```

