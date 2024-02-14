# Setting up Synapse Admin (optional)

The playbook can install and configure [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) for you.

It's a web UI tool you can use to **administrate users and rooms on your Matrix server**. It's designed to work with the Synapse homeserver implementation, but to some extent may work with [Dendrite](./configuring-playbook-dendrite.md) as well.

See the project's [documentation](https://github.com/Awesome-Technologies/synapse-admin) to learn what it does and why it might be useful to you.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_synapse_admin_enabled: true
```

**Note**: Synapse Admin requires Synapse's [Admin APIs](https://matrix-org.github.io/synapse/latest/usage/administration/admin_api/index.html) to function. Access to them is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, for additional security, we normally leave them unexposed, following [official Synapse reverse-proxying recommendations](https://github.com/element-hq/synapse/blob/master/docs/reverse_proxy.md#synapse-administration-endpoints). Because Synapse Admin needs these APIs to function, when installing Synapse Admin, the playbook **automatically** exposes the Synapse Admin API publicly for you. Depending on the homeserver implementation you're using (Synapse, Dendrite), this is equivalent to:

- for [Synapse](./configuring-playbook-synapse.md) (our default homeserver implementation): `matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true`
- for [Dendrite](./configuring-playbook-dendrite.md): `matrix_dendrite_container_labels_public_client_synapse_admin_api_enabled: true`


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

After installation, Synapse Admin will be accessible at: `https://matrix.DOMAIN/synapse-admin/`

To use Synapse Admin, you need to have [registered at least one administrator account](registering-users.md) on your server.

The Homeserver URL to use on Synapse Admin's login page is: `https://matrix.DOMAIN`
