# Setting up a Generic Mautrix Bridge (optional)

The playbook can install and configure various [mautrix](https://github.com/mautrix) bridges (twitter, facebook, instagram, signal, hangouts, googlechat, etc.), as well as many other (non-mautrix) bridges. This is a common guide for configuring mautrix bridges.

You can see each bridge's features at in the `ROADMAP.md` file in its corresponding [mautrix](https://github.com/mautrix) repository.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Replace SERVICENAME with one of: twitter, facebook, instagram, ..
matrix_mautrix_SERVICENAME_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue. Each bridge may have additional requirements besides `_enabled: true`. For example, the mautrix-telegram bridge (our documentation page about it is [here](configuring-playbook-bridge-mautrix-telegram.md)) requires the `matrix_mautrix_telegram_api_id` and `matrix_mautrix_telegram_api_hash` variables to be defined. Refer to each bridge's individual documentation page for details about enabling bridges.

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

## encryption

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

## relay mode

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

## Setting the bot's username

```yaml
matrix_mautrix_SERVICENAME_appservice_bot_username: "BOTNAME"
```

Can be used to set the username for the bridge.

## Discovering additional configuration options

You may wish to look at `roles/custom/matrix-bridge-mautrix-SERVICENAME/templates/config.yaml.j2` and `roles/custom/matrix-bridge-mautrix-SERVICENAME/defaults/main.yml` to find other things you would like to configure.

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

## Set up Double Puppeting

To set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

The bridge automatically performs Double Puppeting if [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) is configured and enabled on the server for this playbook by adding

```yaml
matrix_appservice_double_puppet_enabled: true
```

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

## Controlling the logging level

```yaml
matrix_mautrix_SERVICENAME_logging_level: WARN
```

to `vars.yml` to control the logging level, where you may replace WARN with one of the following to control the verbosity of the logs generated: TRACE, DEBUG, INFO, WARN, ERROR, or FATAL.

If you have issues with a service, and are requesting support, the higher levels of logging will generally be more helpful.

## Usage

To use the bridge, you need to start a chat with `@SERVICENAMEbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login` to the bridge bot to get started. You can learn more here about authentication from the bridge's official documentation on Authentication: https://docs.mau.fi/bridges/python/SERVICENAME/authentication.html

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

## Troubleshooting

For troubleshooting information with a specific bridge, please see the playbook documentation about it (some other document in in `docs/`) and the upstream ([mautrix](https://github.com/mautrix)) bridge documentation for that specific bridge.

Reporting bridge bugs should happen upstream, in the corresponding mautrix repository, not to us.
