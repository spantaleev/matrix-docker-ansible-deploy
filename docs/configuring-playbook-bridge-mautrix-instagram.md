# Setting up Mautrix Instagram bridging (optional, deprecated)

**Note**: This bridge has been deprecated in favor of the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge, which can be installed using [this playbook](configuring-playbook-bridge-mautrix-meta-instagram.md). Consider using that bridge instead of this one.

The playbook can install and configure [mautrix-instagram](https://github.com/mautrix/instagram) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/instagram/index.html) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

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
matrix_admin: "@alice:{{ matrix_domain }}"

# OR:
# The more verbose way. Applies to this bridge only. You may define multiple Matrix users as admins.
matrix_mautrix_instagram_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-instagram/templates/config.yaml.j2` and `roles/custom/matrix-bridge-mautrix-instagram/defaults/main.yml` to find other things you would like to configure.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Usage

To use the bridge, you need to start a chat with `@instagrambot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login YOUR_INSTAGRAM_EMAIL_ADDRESS YOUR_INSTAGRAM_PASSWORD` to the bridge bot to enable bridging for your instagram/Messenger account.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/instagram/authentication.html).
