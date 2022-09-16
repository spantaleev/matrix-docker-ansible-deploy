# Setting up matrix-ldap-registration-proxy (optional)

The playbook can install and configure [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) for you.

This proxy handles Matrix registration requests and forwards them to LDAP.

**Please note:** This does support the full Matrix specification for registrations. It only provide a very coarse
implementation of a basic password registration.

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_ldap_registration_proxy_enabled: true
```
