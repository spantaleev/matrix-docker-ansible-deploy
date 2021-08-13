# Adjusting ma1sd Identity Server configuration (optional)

By default, this playbook configures an [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server for you.

This server is private by default, potentially at the expense of user discoverability.

*ma1sd is a fork of [mxisd](https://github.com/kamax-io/mxisd) which was pronounced end of life 2019-06-21.*

**Note**: enabling ma1sd (which is also the default), means that the `openid` API endpoints will be exposed on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. It's something to be aware of, especially in terms of firewall whitelisting (make sure port `8448` is accessible).


## Disabling ma1sd

ma1sd, being an Identity Server, is not strictly needed. It is only used for 3PIDs (3rd party identifiers like E-mail and phone numbers) and some [enhanced features](https://github.com/ma1uta/ma1sd/#features).

If you'd like for the playbook to not install ma1sd (or to uninstall it if it was previously installed), you can disable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_ma1sd_enabled: false
```

## Matrix.org lookup forwarding

To ensure maximum discovery, you can make your identity server also forward lookups to the central matrix.org Identity server (at the cost of potentially leaking all your contacts information).

Enabling this is discouraged and you'd better [learn more](https://github.com/ma1uta/ma1sd/blob/master/docs/features/identity.md#lookups) before proceeding.

Enabling matrix.org forwarding can happen with the following configuration:

```yaml
matrix_ma1sd_matrixorg_forwarding_enabled: true
```


## Customizing email templates

If you'd like to change the default email templates used by ma1sd, take a look at the `matrix_ma1sd_threepid_medium_email_custom_` variables
(in the `roles/matrix-ma1sd/defaults/main.yml` file.


## ma1sd-controlled Registration

To use the [Registration](https://github.com/ma1uta/ma1sd/blob/master/docs/features/registration.md) feature of ma1sd, you can make use of the following variables:

- `matrix_synapse_enable_registration` - to enable user-initiated registration in Synapse

- `matrix_synapse_enable_registration_captcha` - to validate registering users using reCAPTCHA, as described in the [enabling reCAPTCHA](configuring_captcha.md) documentation.

- `matrix_synapse_registrations_require_3pid` - to control the types of 3pid (`'email'`, `'msisdn'`) required by the Synapse server for registering

- variables prefixed with `matrix_nginx_proxy_proxy_matrix_3pid_registration_` (e.g. `matrix_nginx_proxy_proxy_matrix_3pid_registration_enabled`) - to configure the integrated nginx webserver to send registration requests to ma1sd (instead of Synapse), so it can apply its additional functionality

- `matrix_ma1sd_configuration_extension_yaml` - to configure ma1sd as required. See the [Registration feature's docs](https://github.com/ma1uta/ma1sd/blob/master/docs/features/registration.md) for inspiration. Also see the [Additional features](#additional-features) section below to learn more about how to use `matrix_ma1sd_configuration_extension_yaml`.

**Note**: For this to work, either the homeserver needs to [federate](configuring-playbook-federation.md) or the `openid` APIs need to exposed on the federation port. When federation is disabled and ma1sd is enabled, we automatically expose the `openid` APIs (only!) on the federation port. Make sure the federation port (usually `https://matrix.DOMAIN:8448`) is whitelisted in your firewall (even if you don't actually use/need federation).


## Authentication

[Authentication](https://github.com/ma1uta/ma1sd/blob/master/docs/features/authentication.md) provides the possibility to use your own [Identity Stores](https://github.com/ma1uta/ma1sd/blob/master/docs/stores/README.md) (for example LDAP) to authenticate users on your Homeserver. The following configuration can be used to authenticate against an LDAP server:

```yaml
matrix_synapse_ext_password_provider_rest_auth_enabled: true

# matrix-ma1sd is the hostname of the ma1sd Docker container
matrix_synapse_ext_password_provider_rest_auth_endpoint: "http://matrix-ma1sd:8090"

matrix_ma1sd_configuration_extension_yaml: |
  ldap:
    enabled: true
    connection:
      host: ldapHostnameOrIp
      tls: false
      port: 389
      baseDNs: ['OU=Users,DC=example,DC=org']
      bindDn: CN=My ma1sd User,OU=Users,DC=example,DC=org
      bindPassword: TheUserPassword
```

## Additional features

What this playbook configures for your is some bare minimum Identity Server functionality, so that you won't need to rely on external 3rd party services.

A few variables can be toggled in this playbook to alter the ma1sd configuration that gets generated.

Still, ma1sd can do much more.
You can refer to the [ma1sd website](https://github.com/ma1uta/ma1sd) for more details and configuration options.

To use a more custom configuration, you can define a `matrix_ma1sd_configuration_extension_yaml` string variable
and put your configuration in it.
To learn more about how to do this, refer to the information about `matrix_ma1sd_configuration_extension_yaml` in the [default variables file](../roles/matrix-ma1sd/defaults/main.yml) of the ma1sd component.

## Example: SMS verification

If your use case requires mobile verification, it is quite simple to integrate ma1sd with [Twilio](https://www.twilio.com/), an online telephony services gateway. Their prices are reasonable for low-volume projects and integration can be done with the following configuration:

```yaml
matrix_ma1sd_configuration_extension_yaml: |
  threepid:
    medium:
      msisdn:
        connectors:
          twilio:
            account_sid: '<secret-SID>'
            auth_token: '<secret-token>'
            number: '+<msisdn-number>'
```

## Example: Open Registration for every Domain

If you want to open registration for any domain, you have to setup the allowed domains with ma1sd's `blacklist` and `whitelist`. The default behavior when neither the `blacklist`, nor the `whitelist` match, is to allow registration. Beware: you can't block toplevel domains (aka `.xy`) because the internal architecture of ma1sd doesn't allow that.

```yaml
matrix_ma1sd_configuration_extension_yaml: |
  register:
    policy:
      allowed: true
      threepid:
        email:
          domain:
            blacklist: ~
            whitelist: ~
```

## Troubleshooting

If email address validation emails sent by ma1sd are not reaching you, you should look into [Adjusting email-sending settings](configuring-playbook-email.md).

If you'd like additional logging information, temporarily enable verbose logging for ma1sd.

Example configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`):

```yaml
matrix_ma1sd_verbose_logging: true
```
