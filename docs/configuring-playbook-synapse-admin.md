# Setting up Synapse Admin (optional)

The playbook can install and configure [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) for you.

It's a web UI tool you can use to **administrate users and rooms on your Matrix server**.

See the project's [documentation](https://github.com/Awesome-Technologies/synapse-admin) to learn what it does and why it might be useful to you.

**Warning**: Synapse Admin will likely not work with Synapse v1.32 for now. See [this issue](https://github.com/Awesome-Technologies/synapse-admin/issues/132). If you insist on using Synapse Admin before there's a solution to this issue, you may wish to downgrade Synapse (adding `matrix_synapse_version: v1.31.0` or `matrix_synapse_version_arm64: v1.31.0` to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file).


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_synapse_admin_enabled: true
```

**Note**: Synapse Admin requires Synapse's [Admin APIs](https://github.com/matrix-org/synapse/tree/master/docs/admin_api) to function. Access to them is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, for additional security, we normally leave them unexposed, following [official Synapse reverse-proxying recommendations](https://github.com/matrix-org/synapse/blob/master/docs/reverse_proxy.md#synapse-administration-endpoints). Because Synapse Admin needs these APIs to function, when installing Synapse Admin, we **automatically** exposes them publicly for you (equivalent to `matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled: true`).


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

After installation, Synapse Admin will be accessible at: `https://matrix.DOMAIN/synapse-admin/`

To use Synapse Admin, you need to have [registered at least one administrator account](registering-users.md) on your server.

The Homeserver URL to use on Synapse Admin's login page is: `https://matrix.DOMAIN`

### Sample configuration for running behind Traefik 2.0

Below is a sample configuration for using this playbook with a [Traefik](https://traefik.io/) 2.0 reverse proxy.

This an extension to Traefik config sample in [own-webserver-documentation](./configuring-playbook-own-webserver.md).

```yaml
# Don't bind any HTTP or federation port to the host
# (Traefik will proxy directly into the containers)
matrix_synapse_admin_container_http_host_bind_port: ""

matrix_synapse_admin_container_extra_arguments:
    # May be unnecessary depending on Traefik config, but can't hurt
    - '--label "traefik.enable=true"'

    # The Synapse Admin container will only receive traffic from this subdomain and path
    - '--label "traefik.http.routers.matrix-synapse-admin.rule=(Host(`{{ matrix_server_fqn_matrix }}`) && Path(`{{matrix_synapse_admin_public_endpoint}}`))"'

    # (Define your entrypoint)
    - '--label "traefik.http.routers.matrix-synapse-admin.entrypoints=web-secure"'

    # (The 'default' certificate resolver must be defined in Traefik config)
    - '--label "traefik.http.routers.matrix-synapse-admin.tls.certResolver=default"'

    # The Synapse Admin container uses port 80 by default
    - '--label "traefik.http.services.matrix-synapse-admin.loadbalancer.server.port=80"'
```
