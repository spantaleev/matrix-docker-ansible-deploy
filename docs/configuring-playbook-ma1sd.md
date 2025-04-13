<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 - 2020 MDAD project contributors
SPDX-FileCopyrightText: 2019 Noah Fleischmann
SPDX-FileCopyrightText: 2020 Justin Croonenberghs
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up ma1sd Identity Server (optional)

> [!WARNING]
> Since ma1sd has been unmaintained for years (the latest commit and release being from 2021) and the future of identity server's role in the Matrix specification is uncertain, **we recommend not bothering with installing it unless it's the only way you can do what you need to do**.
>
> Please note that certain things can be achieved with other components. For example, if you wish to implement LDAP integration, you might as well check out [the LDAP provider module for Synapse](./configuring-playbook-ldap-auth.md) instead.

The playbook can configure the [ma1sd](https://github.com/ma1uta/ma1sd) Identity Server for you. It is a fork of [mxisd](https://github.com/kamax-io/mxisd) which was pronounced end of life 2019-06-21.

ma1sd is used for 3PIDs (3rd party identifiers like E-mail and phone numbers) and some [enhanced features](https://github.com/ma1uta/ma1sd/#features). It is private by default, potentially at the expense of user discoverability.

See the project's [documentation](https://github.com/ma1uta/ma1sd/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Open Matrix Federation port

Enabling the ma1sd service will automatically reconfigure your Synapse homeserver to expose the `openid` API endpoints on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. If you enable the component, make sure that the port is accessible.

## Adjusting DNS records

To make the ma1sd Identity Server enable its federation features, set up a SRV record that looks like this:

- Name: `_matrix-identity._tcp` (use this text as-is)
- Content: `10 0 443 matrix.example.com` (replace `example.com` with your own)

See [ma1sd's documentation](https://github.com/ma1uta/ma1sd/wiki/mxisd-and-your-privacy#choices-are-never-easy) for information on the privacy implications of setting up this SRV record.

When setting up a SRV record, if you are asked for a service and protocol instead of a hostname split the host value from the table where the period is. For example use service as `_matrix-identity` and protocol as `_tcp`.

**Note**: This `_matrix-identity._tcp` SRV record for the identity server is different from the `_matrix._tcp` that can be used for Synapse delegation. See [howto-server-delegation.md](howto-server-delegation.md) for more information about delegation.

## Adjusting the playbook configuration

To enable ma1sd, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_ma1sd_enabled: true
```

### Matrix.org lookup forwarding

To ensure maximum discovery, you can make your identity server also forward lookups to the central matrix.org Identity server (at the cost of potentially leaking all your contacts information).

Enabling this is discouraged and you'd better [learn more](https://github.com/ma1uta/ma1sd/blob/master/docs/features/identity.md#lookups) before proceeding.

To enable matrix.org forwarding, add the following configuration to your `vars.yml` file:

```yaml
matrix_ma1sd_matrixorg_forwarding_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-ma1sd/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_ma1sd_configuration_extension_yaml` variable

You can refer to the [ma1sd website](https://github.com/ma1uta/ma1sd) for more details and configuration options.

#### Customizing email templates

If you'd like to change the default email templates used by ma1sd, take a look at the `matrix_ma1sd_threepid_medium_email_custom_` variables (in the `roles/custom/matrix-ma1sd/defaults/main.yml` file.

#### ma1sd-controlled Registration

To use the [Registration](https://github.com/ma1uta/ma1sd/blob/master/docs/features/registration.md) feature of ma1sd, you can make use of the following variables:

- `matrix_synapse_enable_registration` — to enable user-initiated registration in Synapse

- `matrix_synapse_enable_registration_captcha` — to validate registering users using reCAPTCHA, as described in the [enabling reCAPTCHA](configuring-captcha.md) documentation.

- `matrix_synapse_registrations_require_3pid` — a list of 3pid types (among `'email'`, `'msisdn'`) required by the Synapse server for registering

- variables prefixed with `matrix_ma1sd_container_labels_` (e.g. `matrix_ma1sd_container_labels_matrix_client_3pid_registration_enabled`) — to configure the Traefik reverse-proxy to capture and send registration requests to ma1sd (instead of Synapse), so it can apply its additional functionality

- `matrix_ma1sd_configuration_extension_yaml` — to configure ma1sd as required. See the [Registration feature's docs](https://github.com/ma1uta/ma1sd/blob/master/docs/features/registration.md) for inspiration. Also see the [Additional features](#additional-features) section below to learn more about how to use `matrix_ma1sd_configuration_extension_yaml`.

**Note**: For this to work, either the homeserver needs to [federate](configuring-playbook-federation.md) or the `openid` APIs need to exposed on the federation port. When federation is disabled and ma1sd is enabled, we automatically expose the `openid` APIs (only!) on the federation port. Make sure the federation port (usually `https://matrix.example.com:8448`) is whitelisted in your firewall (even if you don't actually use/need federation).

#### Authentication

[Authentication](https://github.com/ma1uta/ma1sd/blob/master/docs/features/authentication.md) provides the possibility to use your own [Identity Stores](https://github.com/ma1uta/ma1sd/blob/master/docs/stores/README.md) (for example LDAP) to authenticate users on your Homeserver.

To enable authentication against an LDAP server, add the following configuration to your `vars.yml` file:

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

#### Example: SMS verification

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

#### Example: Open Registration for every Domain

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

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

If email address validation emails sent by ma1sd are not reaching you, you should look into [Adjusting email-sending settings](configuring-playbook-email.md).

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-ma1sd`.

### Increase logging verbosity

If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# See: https://github.com/ma1uta/ma1sd/blob/master/docs/troubleshooting.md#increase-verbosity
matrix_ma1sd_verbose_logging: true
```
