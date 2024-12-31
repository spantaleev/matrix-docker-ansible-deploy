# Setting up Mautrix Signal bridging (optional)

The playbook can install and configure [mautrix-signal](https://github.com/mautrix/signal) for you.

See the project's [documentation](https://docs.mau.fi/bridges/python/signal/index.html) to learn what it does and why it might be useful to you.

## Prerequisites (optional)

### Prepare Postgres database on external Postgres server

If you're running with the Postgres database server integrated by the playbook (which is the default), you don't need to do anything special and can easily proceed with installing.

However, if you're [using an external Postgres server](configuring-playbook-external-postgres.md), you'd need to manually prepare a Postgres database for this bridge and adjust the variables related to that (`matrix_mautrix_signal_database_*`).

### Enable Appservice Double Puppet

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_mautrix_signal_enabled: true
```

### Bridge permissions

By default, any user on your homeserver will be able to use the bridge.

Different levels of permission can be granted to users:

- `relay` - Allowed to be relayed through the bridge, no access to commands
- `user` - Use the bridge with puppeting
- `admin` - Use and administer the bridge

The permissions are following the sequence: nothing < `relay` < `user` < `admin`.

The default permissions are set via `matrix_mautrix_signal_bridge_permissions` and are somewhat like this:

```yaml
matrix_mautrix_signal_bridge_permissions:
  '*': relay
  example.com: user
  '{{ matrix_admin }}': admin
```

In case you want to replace the default permissions settings **completely**, populate the following item within your `vars.yml` file:

```yaml
matrix_mautrix_signal_bridge_permissions:
  '@alice:{{ matrix_domain }}': admin
  '@bob:{{ matrix_domain }}' : user
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#setting-the-bot-s-username-optional), etc.

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
