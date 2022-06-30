# Setting up Mautrix Instagram (optional)

The playbook can install and configure [mautrix-instagram](https://github.com/mautrix/instagram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/instagram/index.html) to learn what it does and why it might be useful to you.

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
      '@YOUR_USERNAME:YOUR_DOMAIN': admin
```

You may wish to look at `roles/matrix-bridge-mautrix-instagram/templates/config.yaml.j2` and `roles/matrix-bridge-mautrix-instagram/defaults/main.yml` to find other things you would like to configure.


## Usage

You then need to start a chat with `@instagrambot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `login YOUR_INSTAGRAM_EMAIL_ADDRESS YOUR_INSTAGRAM_PASSWORD` to the bridge bot to enable bridging for your instagram/Messenger account.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/instagram/authentication.html).
