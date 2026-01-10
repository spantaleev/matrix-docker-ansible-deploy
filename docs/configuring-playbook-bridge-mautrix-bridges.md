<!--
SPDX-FileCopyrightText: 2022 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2022 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up a Generic Mautrix Bridge (optional)

The playbook can install and configure various [mautrix](https://github.com/mautrix) bridges (twitter, discord, signal, googlechat, etc.), as well as many other (non-mautrix) bridges. This is a common guide for configuring mautrix bridges.

The author of the bridges maintains [the official docs](https://docs.mau.fi/bridges/index.html), whose source code is available at [mautrix/docs](https://github.com/mautrix/docs) repository on GitHub. You may as well to refer it while configuring them.

You can see each bridge's features on the `ROADMAP.md` file in its corresponding mautrix repository.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Replace SERVICENAME with one of: twitter, discord, signal, googlechat, etc.
matrix_mautrix_SERVICENAME_enabled: true
```

**Note**: for bridging to Meta's Messenger or Instagram, you would need to add `meta` with an underscore symbol (`_`) or hyphen (`-`) based on the context as prefix to each `SERVICENAME`; add `_` to variables (as in `matrix_mautrix_meta_messenger_configuration_extension_yaml` for example) and `-` to paths of the configuration files (as in `roles/custom/matrix-bridge-mautrix-meta-messenger/templates/config.yaml.j2`), respectively.

There are some additional things you may wish to configure about the bridge before you continue. Each bridge may have additional requirements besides `_enabled: true`. For example, the mautrix-telegram bridge (our documentation page about it is [here](configuring-playbook-bridge-mautrix-telegram.md)) requires the `matrix_mautrix_telegram_api_id` and `matrix_mautrix_telegram_api_hash` variables to be defined. Refer to each bridge's individual documentation page for details about enabling bridges.

### Configure bridge permissions (optional)

By default any user on your homeserver will be able to use the mautrix bridges. To limit who can use them you would need to configure their permissions settings.

Different levels of permission can be granted to users. For example, to **configure a user as an administrator for all bridges**, add the following configuration to your `vars.yml` file:

```yaml
matrix_admin: "@alice:{{ matrix_domain }}"
```

If you don't define the `matrix_admin` in your configuration (e.g. `matrix_admin: @alice:example.com`), then there's no admin by default.

**Alternatively** (more verbose, but allows multiple admins to be configured), you can do the same on a per-bridge basis with:

```yaml
matrix_mautrix_SERVICENAME_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
```

This will add the admin permission to the specific user, while keeping the default permissions.

You could also redefine the default permissions settings completely, rather than adding extra permissions. You may wish to look at `roles/custom/matrix-bridge-mautrix-SERVICENAME/templates/config.yaml.j2` to find information on the permission settings and other options you would like to configure.

### Enable encryption (optional)

[Encryption (End-to-Bridge Encryption, E2BE) support](https://docs.mau.fi/bridges/general/end-to-bridge-encryption.html) is off by default. If you would like to enable encryption, add the following configuration to your `vars.yml` file:

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

[Relay mode](https://docs.mau.fi/bridges/general/relay-mode.html) is off by default. Check [the table on the official documentation](https://docs.mau.fi/bridges/general/relay-mode.html#support-table) for bridges which support relay mode.

If you would like to enable it, add the following configuration to your `vars.yml` file:

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
    relay:
      enabled: true
    permissions:
      '@alice:{{ matrix_domain }}': admin
    encryption:
      allow: true
      default: true
```

If you want to activate the relaybot in a room, send `!prefix set-relay` in the rooms where you want to use the bot (replace `!prefix` with the appropriate command prefix for the bridge, like `!signal` or `!wa`). To deactivate, send `!prefix unset-relay`.

Use `!prefix set-pl 100` to be able for the bot to modify room settings and invite others.

#### Allow anyone on the homeserver to become a relay user (optional)

By default, only admins are allowed to set themselves as relay users. To allow anyone on your homeserver to set themselves as relay users, add the following configuration to your `vars.yml` file:

```yaml
matrix_mautrix_SERVICENAME_bridge_relay_admin_only: false
```

### Set the bot's username (optional)

To set the bot's username, add the following configuration to your `vars.yml` file:

```yaml
matrix_mautrix_SERVICENAME_appservice_bot_username: "BOTNAME"
```

### Configure the logging level (optional)

To specify the logging level, add the following configuration to your `vars.yml` file:

```yaml
matrix_mautrix_SERVICENAME_logging_level: warn
```

Replace `warn` with one of the following to control the verbosity of the logs generated: `trace`, `debug`, `info`, `warn`, `error` or `fatal`.

If you have issues with a service, and are requesting support, the higher levels of logging (those that appear earlier in the list, like `trace`) will generally be more helpful.

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-mautrix-SERVICENAME/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-mautrix-SERVICENAME/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_mautrix_SERVICENAME_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@SERVICENAMEbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

For details about the next steps, refer to each bridge's individual documentation page.

Send `help` to the bot to see the available commands.

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

### Set up Double Puppeting (optional)

After successfully enabling bridging, you may wish to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do).

To set it up, you have 2 ways of going about it.

#### Method 1: automatically, by enabling Appservice Double Puppet (recommended)

To set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html), you could enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

Appservice Double Puppet is a homeserver appservice through which bridges (and potentially other services) can impersonate any user on the homeserver.

To enable the Appservice Double Puppet service, add the following configuration to your `vars.yml` file:

```yaml
matrix_appservice_double_puppet_enabled: true
```

When enabled, double puppeting will automatically be enabled for all bridges that support double puppeting via the appservice method.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

**Notes**:

- Previously there were multiple different automatic double puppeting methods like one with the help of the [Shared Secret Auth password provider module](./configuring-playbook-shared-secret-auth.md), but they have been superseded by this Appservice Double Puppet method. Double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future as the older methods were completely removed in the megabridge rewrites on [the upstream project](https://docs.mau.fi/bridges/general/double-puppeting.html#automatically).

<!-- TODO: remove this note if the Shared Secret Auth service has stopped working or the bridges have been removed -->
- Some bridges like [the deprecated Facebook mautrix bridge](configuring-playbook-bridge-mautrix-facebook.md) and [matrix-appservice-kakaotalk](configuring-playbook-bridge-appservice-kakaotalk.md), which is partially based on the Facebook bridge, are compatible with the Shared Secret Auth service only. These bridges automatically perform Double Puppeting if [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service is configured and enabled on the server for this playbook.

#### Method 2: manually, by asking each user to provide a working access token

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to obtain one](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the session for which you obtained an access token some time in the future, as that would break the Double Puppeting feature

## Troubleshooting

For troubleshooting information with a specific bridge, please see the playbook documentation about it (some other document in in `docs/`) and the upstream ([mautrix](https://github.com/mautrix)) bridge documentation for that specific bridge.

If the bridge's bot doesn't accept the invite to a chat, refer [the official troubleshooting page](https://docs.mau.fi/bridges/general/troubleshooting.html) as well.

If you found bugs in mautrix bridges, they should be reported to the upstream project, in the corresponding mautrix repository, not to us.
