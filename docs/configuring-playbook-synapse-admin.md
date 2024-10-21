# Setting up Synapse Admin (optional)

The playbook can install and configure [etkecc/synapse-admin](https://github.com/etkecc/synapse-admin) (a [feature-rich](https://github.com/etkecc/synapse-admin#fork-differences) fork of [Awesome-Technologies/synapse-admin](https://github.com/Awesome-Technologies/synapse-admin)) for you.

synapse-admin is a web UI tool you can use to **administrate users, rooms, media, etc. on your Matrix server**. It's designed to work with the Synapse homeserver implementation, but to some extent may work with [Dendrite](./configuring-playbook-dendrite.md) as well.

See the project's [documentation](https://github.com/etkecc/synapse-admin) to learn what it does and why it might be useful to you.


## Adjusting the playbook configuration

To enable Synapse Admin, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_admin_enabled: true
```

**Note**: Synapse Admin requires Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/usage/administration/admin_api/index.html) to function. Access to them is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, for additional security, we normally leave them unexposed, following [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints). Because Synapse Admin needs these APIs to function, when installing Synapse Admin, the playbook **automatically** exposes the Synapse Admin API publicly for you. Depending on the homeserver implementation you're using (Synapse, Dendrite), this is equivalent to:

- for [Synapse](./configuring-playbook-synapse.md) (our default homeserver implementation): `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true`
- for [Dendrite](./configuring-playbook-dendrite.md): `matrix_dendrite_container_labels_public_client_synapse_admin_api_enabled: true`

By default, synapse-admin installation will be [restricted to only work with one homeserver](https://github.com/etkecc/synapse-admin/blob/e21e44362c879ac41f47c580b04210842b6ff3d7/README.md#restricting-available-homeserver) - the one managed by the playbook. To adjust these restrictions, tweak the `matrix_synapse_admin_config_restrictBaseUrl` variable.

⚠ **Warning**: If you're using [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md) (MAS) for authentication, you will be able to [log into synapse-admin with an access token](https://github.com/etkecc/synapse-admin/pull/58), but certain synapse-admin features (especially those around user management) will be limited or not work at all.

### Adjusting the Synapse Admin URL

By default, this playbook installs Synapse Admin on the `matrix.` subdomain, at the `/synapse-admin` path (https://matrix.example.com/synapse-admin). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_synapse_admin_hostname` and `matrix_synapse_admin_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_synapse_admin_hostname: admin.example.com
matrix_synapse_admin_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the Synapse Admin domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command:

## Usage

After installation, Synapse Admin will be accessible at: `https://matrix.example.com/synapse-admin/`

To use Synapse Admin, you need to have [registered at least one administrator account](registering-users.md) on your server.
