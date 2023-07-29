# Setting up Synapse Admin (optional)

The playbook can install and configure [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) for you.

It's a web UI tool you can use to **administrate users and rooms on your Matrix server**.

See the project's [documentation](https://github.com/Awesome-Technologies/synapse-admin) to learn what it does and why it might be useful to you.


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

### Sample configuration for running behind Caddy v2

Below is a sample configuration for using this playbook with a [Caddy](https://caddyserver.com/v2) 2.0 reverse proxy (non-default configuration where `matrix-nginx-proxy` is disabled - `matrix_nginx_proxy_enabled: false`).

```caddy
# This is a basic configuration that will function the same as the default nginx proxy - exposing the synapse-admin panel to matrix.YOURSERVER.com/synapse-admin/
  handle_path /synapse-admin* {
        reverse_proxy localhost:8766  {
        }
  }
```
