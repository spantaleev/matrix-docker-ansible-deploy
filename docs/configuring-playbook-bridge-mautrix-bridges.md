# Setting up a Generic Mautrix Bridge (optional)

The playbook can install and configure various [mautrix](https://github.com/mautrix) bridges (twitter, discord, signal, googlechat, etc.), as well as many other (non-mautrix) bridges. This is a common guide for configuring mautrix bridges.

You can see each bridge's features at in the `ROADMAP.md` file in its corresponding [mautrix](https://github.com/mautrix) repository.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Replace SERVICENAME with one of: twitter, discord, signal, googlechat, etc.
matrix_mautrix_SERVICENAME_enabled: true
```

**Note**: for bridging to Meta's Messenger or Instagram, you would need to add `meta` with an underscore symbol (`_`) or hyphen (`-`) based on the context as prefix to each `SERVICENAME`; add `_` to variables (as in `matrix_mautrix_meta_messenger_configuration_extension_yaml` for example) and `-` to paths of the configuration files (as in `roles/custom/matrix-bridge-mautrix-meta-messenger/templates/config.yaml.j2`), respectively. **`matrix_mautrix_facebook_*` and `matrix_mautrix_instagram_*` variables belong to the deprecated components and do not control the new bridge** ([mautrix-meta](https://github.com/mautrix/meta)), which can be installed using [this playbook](configuring-playbook-bridge-mautrix-meta-messenger.md).

There are some additional things you may wish to configure about the bridge before you continue. Each bridge may have additional requirements besides `_enabled: true`. For example, the mautrix-telegram bridge (our documentation page about it is [here](configuring-playbook-bridge-mautrix-telegram.md)) requires the `matrix_mautrix_telegram_api_id` and `matrix_mautrix_telegram_api_hash` variables to be defined. Refer to each bridge's individual documentation page for details about enabling bridges.

### Configure bridge permissions (optional)

To **configure a user as an administrator for all bridges**, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_admin: "@alice:{{ matrix_domain }}"
```

**Alternatively** (more verbose, but allows multiple admins to be configured), you can do the same on a per-bridge basis with:

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
```

### Enable encryption (optional)

Encryption support is off by default. If you would like to enable encryption, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

**for all bridges with encryption support**:

```yaml
matrix_bridges_encryption_enabled: true
matrix_bridges_encryption_default: true
```

**Alternatively**, for a specific bridge:

```yaml
matrix_mautrix_SERVICENAME_bridge_encryption_enabled: true
matrix_mautrix_SERVICENAME_bridge_encryption_default: true
```

### Enable relay mode (optional)

Relay mode is off by default. If you would like to enable relay mode, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

**for all bridges with relay mode support**:

```yaml
matrix_bridges_relay_enabled: true
```

**Alternatively**, for a specific bridge:

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    relay:
      enabled: true
```

You can only have one `matrix_mautrix_SERVICENAME_configuration_extension_yaml` definition in `vars.yml` per bridge, so if you need multiple pieces of configuration there, just merge them like this:

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
    encryption:
      allow: true
      default: true
```

### Set the bot's username (optional)

To set the bot's username, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_SERVICENAME_appservice_bot_username: "BOTNAME"
```

### Configure the logging level (optional)

To specify the logging level, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_SERVICENAME_logging_level: WARN
```

Replace WARN with one of the following to control the verbosity of the logs generated: TRACE, DEBUG, INFO, WARN, ERROR, or FATAL.

If you have issues with a service, and are requesting support, the higher levels of logging will generally be more helpful.

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-mautrix-SERVICENAME/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-mautrix-SERVICENAME/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_mautrix_SERVICENAME_configuration_extension_yaml` variable

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

To use the bridge, you need to start a chat with `@SERVICENAMEbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login` to the bridge bot to get started. You can learn more here about authentication from the bridge's official documentation on Authentication: https://docs.mau.fi/bridges/python/SERVICENAME/authentication.html

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

### Set up Double Puppeting (optional)

To set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

The bridge automatically performs Double Puppeting if [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) is configured and enabled on the server for this playbook by adding the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_double_puppet_enabled: true
```

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

## Troubleshooting

For troubleshooting information with a specific bridge, please see the playbook documentation about it (some other document in in `docs/`) and the upstream ([mautrix](https://github.com/mautrix)) bridge documentation for that specific bridge.

Reporting bridge bugs should happen upstream, in the corresponding mautrix repository, not to us.
