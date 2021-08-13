# Controlling Matrix federation (optional)

By default, your server federates with the whole Matrix network.
That is, people on your server can communicate with people on any other Matrix server.


## Federating only with select servers

To make your server only federate with servers of your choosing, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_federation_domain_whitelist:
- example.com
- another.com
```

If you wish to disable federation, you can do that with an empty list (`[]`), or better yet by completely disabling federation (see below).


## Exposing the room directory over federation

By default, your server's public rooms directory is not exposed to other servers via federation.

If you wish to expose it, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_allow_public_rooms_over_federation: true
```


## Disabling federation

To completely disable federation, isolating your server from the rest of the Matrix network, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_federation_enabled: false
```

With that, your server's users will only be able to talk among themselves, but not to anyone who is on another server.

**Disabling federation does not necessarily disable the federation port** (`8448`). Services like [Dimension](configuring-playbook-dimension.md) and [ma1sd](configuring-playbook-ma1sd.md) normally rely on `openid` APIs exposed on that port. Even if you disable federation and only if necessary, we may still be exposing the federation port and serving the `openid` APIs there. To override this and completely disable Synapse's federation port use:

```yaml
# This stops the federation port on the Synapse side (normally `matrix-synapse:8048` on the container network).
matrix_synapse_federation_port_enabled: false

# This removes the `8448` virtual host from the matrix-nginx-proxy reverse-proxy server.
matrix_nginx_proxy_proxy_matrix_federation_api_enabled: false
```
