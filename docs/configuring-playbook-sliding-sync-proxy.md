# Setting up the Sliding Sync proxy (optional)

The playbook can install and configure [sliding-sync](https://github.com/matrix-org/sliding-sync) proxy for you.

Sliding Sync is an implementation of [MSC3575](https://github.com/matrix-org/matrix-spec-proposals/blob/kegan/sync-v3/proposals/3575-sync.md) and a prerequisite for running the new (**still beta**) Element X clients ([Element X iOS](https://github.com/element-hq/element-x-ios) and [Element X Android](https://github.com/element-hq/element-x-android)).

See the project's [documentation](https://github.com/matrix-org/sliding-sync) to learn more.

Element X iOS is [available on TestFlight](https://testflight.apple.com/join/uZbeZCOi).

Element X Android is [available on the Github Releases page](https://github.com/element-hq/element-x-android/releases).

**Note**: The sliding-sync proxy is **not required** when using the **Conduit homeserver**. Starting from version `0.6.0` Conduit has native support for some sliding sync features. If there are issues with the native implementation, you might have a better experience when enabling the sliding-sync proxy anyway.

## Adjusting the playbook configuration

To enable Sliding Sync proxy, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_sliding_sync_enabled: true
```

### Adjusting the Sliding Sync proxy URL

By default, this playbook installs the Sliding Sync proxy on the `matrix.` subdomain, at the `/sliding-sync` path (https://matrix.example.com/sliding-sync). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_sliding_sync_hostname` and `matrix_sliding_sync_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_sliding_sync_hostname: ss.example.com
matrix_sliding_sync_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the Honoroit domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all`.

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

You **don't need to do anything special** to make use of the Sliding Sync proxy. Simply open your client which supports Sliding Sync (like Element X) and log in.

When the Sliding Sync proxy is [installed](#installing), your `/.well-known/matrix/client` file is also updated. A new `org.matrix.msc3575.proxy` section and `url` property are added there and made to point to your Sliding Sync proxy's base URL (e.g. `https://matrix.example.com/sliding-sync`).

This allows clients which support Sliding Sync to detect the Sliding Sync proxy's URL and make use of it.
