# Setting up Sliding Sync Proxy (optional)

The playbook can install and configure [sliding-sync](https://github.com/matrix-org/sliding-sync) proxy for you.

Sliding Sync is an implementation of [MSC3575](https://github.com/matrix-org/matrix-spec-proposals/blob/kegan/sync-v3/proposals/3575-sync.md) and a prerequisite for running the new (**still beta**) Element X clients ([Element X iOS](https://github.com/element-hq/element-x-ios) and [Element X Android](https://github.com/element-hq/element-x-android)).

See the project's [documentation](https://github.com/matrix-org/sliding-sync) to learn more.

Element X iOS is [available on TestFlight](https://testflight.apple.com/join/uZbeZCOi).

Element X Android is [available on the Github Releases page](https://github.com/element-hq/element-x-android/releases).

**NOTE**: The sliding-sync proxy is **not required** when using the **Conduit homeserver**. Starting from version `0.6.0` Conduit has native support for some sliding sync features. If there are issues with the native implementation, you might have a better experience when enabling the sliding-sync proxy anyway.

## Decide on a domain and path

By default, the Sliding Sync proxy is configured to be served on the Matrix domain (`matrix.DOMAIN`, controlled by `matrix_server_fqn_matrix`), under the `/sliding-sync` path.

This makes it easy to set it up, **without** having to [adjust your DNS records](#adjusting-dns-records).

If you'd like to run the Sliding Sync proxy on another hostname or path, use the `matrix_sliding_sync_hostname` and `matrix_sliding_sync_path_prefix` variables.


## Adjusting DNS records

If you've changed the default hostame, **you may need to adjust your DNS** records.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_sliding_sync_enabled: true
```


## Installing

After potentially [adjusting DNS records](#adjusting-dns-records) and configuring the playbook, run the [installation](installing.md) command again: `just install-all`.

### External databases

Please note that, if your setup utilizes an external database, you must also establish configuration for the sliding sync proxy. Alter the defaults below to suit your configuration:

```yaml
matrix_sliding_sync_database_username: 'matrix_sliding_sync'
matrix_sliding_sync_database_password: ''
matrix_sliding_sync_database_hostname: ''
matrix_sliding_sync_database_port: 5432
matrix_sliding_sync_database_name: 'matrix_sliding_sync'
```

## Usage

You **don't need to do anything special** to make use of the Sliding Sync Proxy.
Simply open your client which supports Sliding Sync (like Element X) and log in.

When the Sliding Sync proxy is [installed](#installing), your `/.well-known/matrix/client` file is also updated. A new `org.matrix.msc3575.proxy` section and `url` property are added there and made to point to your Sliding Sync proxy's base URL (e.g. `https://matrix.DOMAIN/sliding-sync`).

This allows clients which support Sliding Sync to detect the Sliding Sync Proxy's URL and make use of it.
