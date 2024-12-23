# Setting up Mautrix Signal bridging (optional)

The playbook can install and configure [mautrix-signal](https://github.com/mautrix/signal) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/signal/index.html) to learn what it does and why it might be useful to you.

**Note**: This revamped version of the [mautrix-signal (legacy)](configuring-playbook-bridge-mautrix-signal.md) may increase the CPU usage of your homeserver.

## Prerequisites (optional)

### Prepare Postgres database on external Postgres server

If you're running with the Postgres database server integrated by the playbook (which is the default), you don't need to do anything special and can easily proceed with installing.

However, if you're [using an external Postgres server](configuring-playbook-external-postgres.md), you'd need to manually prepare a Postgres database for this bridge and adjust the variables related to that (`matrix_mautrix_signal_database_*`).

### Enable Appservice Double Puppet

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

For details about configuring Double Puppeting for this bridge, see the section below: [Set up Double Puppeting](#-set-up-double-puppeting)

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_signal_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue.

By default, any user on your homeserver will be able to use the bridge.

Different levels of permission can be granted to users:

* relay - Allowed to be relayed through the bridge, no access to commands;
* user - Use the bridge with puppeting;
* admin - Use and administer the bridge.

The permissions are following the sequence: nothing < relay < user < admin.

The default permissions are set as follows:

```yaml
permissions:
  '*': relay
  example.com: user
```

If you want to augment the preset permissions, you might want to set the additional permissions with the following settings in your `vars.yml` file:

```yaml
matrix_mautrix_signal_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
```

This will add the admin permission to the specific user, while keeping the default permissions.

In case you want to replace the default permissions settings **completely**, populate the following item within your `vars.yml` file:

```yaml
matrix_mautrix_signal_bridge_permissions:
  '@alice:{{ matrix_domain }}': admin
  '@bob:{{ matrix_domain }}' : user
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-signal/templates/config.yaml.j2` to find more information on the permissions settings and other options you would like to configure.

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

To use the bridge, you need to start a chat with `@signalbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

### 💡 Set up Double Puppeting

After successfully enabling bridging, you may wish to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do).

To set it up, you have 2 ways of going about it.

#### Method 1: automatically, by enabling Appservice Double Puppet

The bridge automatically performs Double Puppeting if [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service is configured and enabled on the server for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

#### Method 2: manually, by asking each user to provide a working access token

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to obtain one](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Signal` device some time in the future, as that would break the Double Puppeting feature
