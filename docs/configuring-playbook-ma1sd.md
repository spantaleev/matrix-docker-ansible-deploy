# Adjusting mxisd Identity Server configuration (optional)

By default, this playbook configures an [mxisd](https://github.com/kamax-io/mxisd) Identity Server for you.

This server is private by default, potentially at the expense of user discoverability.


## Matrix.org lookup forwarding

To ensure maximum discovery, you can make your identity server also forward lookups to the central matrix.org Identity server (at the cost of potentially leaking all your contacts information).

Enabling this is discouraged and you'd better [learn more](https://github.com/kamax-io/mxisd/blob/master/docs/features/identity.md#lookups) before proceeding.

Enabling matrix.org forwarding can happen with the following configuration:

```yaml
matrix_mxisd_matrixorg_forwarding_enabled: true
```


## Customizing email templates

If you'd like to change the default email templates used by mxisd, take a look at the `matrix_mxisd_threepid_medium_email_custom_` variables
(in the `roles/matrix-mxisd/defaults/main.yml` file.


## mxisd-controlled Registration

To use the [Registration](https://github.com/kamax-matrix/mxisd/blob/master/docs/features/registration.md) feature of mxisd, you can make use of the following variables:

- `matrix_synapse_enable_registration` - to enable user-initiated registration in Synapse

- `matrix_synapse_registrations_require_3pid` - to control the types of 3pid (`'email'`, `'msisdn'`) required by the Synapse server for registering

- variables prefixed with `matrix_nginx_proxy_proxy_matrix_3pid_registration_` (e.g. `matrix_nginx_proxy_proxy_matrix_3pid_registration_enabled`) - to configure the integrated nginx webserver to send registration requests to mxisd (instead of Synapse), so it can apply its additional functionality

- `matrix_mxisd_configuration_extension_yaml` - to configure mxisd as required. See the [Registration feature's docs](https://github.com/kamax-matrix/mxisd/blob/master/docs/features/registration.md) for inspiration. Also see the [Additional features](#additional-features) section below to learn more about how to use `matrix_mxisd_configuration_extension_yaml`.

## Authentication

[Authentication](https://github.com/kamax-matrix/mxisd/blob/master/docs/features/authentication.md) provides the possibility to use your own [Identity Stores](https://github.com/kamax-matrix/mxisd/blob/master/docs/stores/README.md) (for example LDAP) to authenticate users on your Homeserver. The following configuration can be used to authenticate against an LDAP server:

```yaml
matrix_synapse_ext_password_provider_rest_auth_enabled: true

# matrix-mxisd is the hostname of the mxisd Docker container
matrix_synapse_ext_password_provider_rest_auth_endpoint: "http://matrix-mxisd:8090"

matrix_mxisd_configuration_extension_yaml: |
  ldap:
    enabled: true
    connection:
      host: ldapHostnameOrIp
      tls: false
      port: 389
      baseDNs: ['OU=Users,DC=example,DC=org']
      bindDn: CN=My Mxisd User,OU=Users,DC=example,DC=org
      bindPassword: TheUserPassword
```

## Additional features

What this playbook configures for your is some bare minimum Identity Server functionality, so that you won't need to rely on external 3rd party services.

A few variables can be toggled in this playbook to alter the mxisd configuration that gets generated.

Still, mxisd can do much more.
You can refer to the [mxisd website](https://github.com/kamax-io/mxisd) for more details and configuration options.

To use a more custom configuration, you can define a `matrix_mxisd_configuration_extension_yaml` string variable
and put your configuration in it.
To learn more about how to do this, refer to the information about `matrix_mxisd_configuration_extension_yaml` in the [default variables file](../roles/matrix-mxisd/defaults/main.yml) of the mxisd component.


## Troubleshooting

If email address validation emails sent by mxisd are not reaching you, you should look into [Adjusting email-sending settings](configuring-playbook-email.md).

If you'd like additional logging information, temporarily enable verbose logging for mxisd.

Example configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`):

```yaml
matrix_mxisd_verbose_logging: true
```