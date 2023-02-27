# Nginx reverse-proxy fronting playbook's Traefik

This directory contains a sample config that show you how to do reverse-proxying using Nginx and the playbook's internal traefik container.

This is for when you wish to front the playbook's integrated traefik container with a self-managed Nginx reverse-proxy running on the same server.
See the [Using your own webserver, instead of this playbook's nginx proxy & Fronting the integrated reverse-proxy webserver with another reverse-proxy](../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) documentation page and follow the instructions for the playbook's configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`).

That is this part:
**For Traefik** fronted by another reverse-proxy, you would need some configuration like this:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik

# Ensure that public urls use https
matrix_playbook_ssl_enabled: true

# Disable the web-secure (port 443) endpoint, which also disables SSL certificate retrieval
devture_traefik_config_entrypoint_web_secure_enabled: false

devture_traefik_container_web_host_bind_port: '127.0.0.1:81'

devture_traefik_additional_entrypoints_auto:
  - name: matrix-federation
    port: 8449
    host_bind_port: '127.0.0.1:8449'
    config: {}
```

**NOTE**: 
- that this also disables SSL certificate retrieval, which then has to be done manually (e.g. by using certbot and setting the appropriate path as found in [the example nginx configuration file](./matrix.conf)). For the example nginx config one certificate is used that contains all the used subdomains.
- that [the example nginx configuration file](./matrix.conf) has to be adapted to whatever services you are using. For example, remove element.domain.com from the `server_name` list if you don't use Element web client or add dimension.domain.com to it if you do use Dimension.
- that this is just an example and may not be entirely accurate. It may also not cover other use cases (enabling various services or bridges requires additional reverse-proxying configuration).
