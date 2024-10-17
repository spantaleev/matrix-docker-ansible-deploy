# Setting up Mautrix Instagram (optional)

**Note**: bridging to Facebook [Instagram](https://instagram.com) via this bridge is being [superseded by a new bridge - mautrix-meta](https://github.com/mautrix/facebook/issues/332). For now, the mautrix-instagram bridge continues to work, but the new [mautrix-meta-instagram bridge](./configuring-playbook-bridge-mautrix-meta-instagram.md) is better and more supported. Consider using that bridge instead of this one.

The playbook can install and configure [mautrix-instagram](https://github.com/mautrix/instagram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/instagram/index.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_mautrix_instagram_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue.

Encryption support is off by default. If you would like to enable encryption, add the following to your `vars.yml` file:
```yaml
matrix_mautrix_instagram_configuration_extension_yaml: |
  bridge:
    encryption:
      allow: true
      default: true
```

If you would like to be able to administrate the bridge from your account it can be configured like this:
```yaml
# The easy way. The specified Matrix user ID will be made an admin of all bridges
matrix_admin: "@YOUR_USERNAME:{{ matrix_domain }}"

# OR:
# The more verbose way. Applies to this bridge only. You may define multiple Matrix users as admins.
matrix_mautrix_instagram_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:example.com': admin
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-instagram/templates/config.yaml.j2` and `roles/custom/matrix-bridge-mautrix-instagram/defaults/main.yml` to find other things you would like to configure.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

You then need to start a chat with `@instagrambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login YOUR_INSTAGRAM_EMAIL_ADDRESS YOUR_INSTAGRAM_PASSWORD` to the bridge bot to enable bridging for your instagram/Messenger account.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/instagram/authentication.html).
