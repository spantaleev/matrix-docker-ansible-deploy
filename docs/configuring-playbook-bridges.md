# Setting up a Generic Mautrix Bridge (optional)

The playbook can install and configure bridges with mautrix (Currently twitter, facebook, instagram, signal, hangouts, googlechat)


You can see each bridge features at https://github.com/mautrix/SERVICENAME/blob/master/ROADMAP.md

To enable a bridge add


```yaml
matrix_mautrix_SERVICENAME_enabled: true
```

to your `vars.yml`

There are some additional things you may wish to configure about the bridge before you continue.

You can add

```yaml
matrix_admin: "@YOUR_USERNAME:{{ matrix_domain }}"
```
to 'vars.yml' to configure a user as administrator for all bridges, or you prefer to do it bridge by bridge you can configure it with

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:{{ matrix_domain }}': admin
```

Encryption support is off by default. If you would like to enable encryption, add the following to your `vars.yml` file:
```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    encryption:
      allow: true
      default: true
```


Using both would look like

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:{{ matrix_domain }}': admin
    encryption:
      allow: true
      default: true
```

```yaml
matrix_mautrix_SERVICENAME_appservice_bot_username: "BOTNAME"
```

Can be used to set the username for the bridge.


You may wish to look at `roles/matrix-bridge-mautrix-SERVICENAME/templates/config.yaml.j2` and `roles/matrix-bridge-mautrix-SERVICENAME/defaults/main.yml` to find other things you would like to configure.


## Set up Double Puppeting

To set up  [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html)

please do so automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook by adding

```yaml
matrix_synapse_ext_password_provider_shared_secret_auth_enabled: true
matrix_synapse_ext_password_provider_shared_secret_auth_shared_secret: YOUR_SHARED_SECRET_GOES_HERE
```

You should generate a strong shared secret with a command like this: pwgen -s 64 1

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.



## Usage

You then need to start a chat with `@SERVICENAMEbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain). 

Send `login ` to the bridge bot to get started You can learn more here about authentication from the bridge's official documentation on Authentication https://docs.mau.fi/bridges/python/SERVICENAME/authentication.html  .

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.



## Troubleshooting

Please see SERVICENAME's individual doc page for troubleshooting information.
