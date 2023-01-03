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

# This stops the federation port on the synapse-reverse-proxy-companion side (normally `matrix-synapse-reverse-proxy-companion:8048` on the container network).
matrix_synapse_reverse_proxy_companion_federation_api_enabled: false
```

## Changing the federation port from 8448 to a different port to use a CDN that only accepts 443/80 ports

Why? This change could be useful for people running small Synapse instances on small severs/VPSes to avoid being impacted by a simple DOS/DDOS when bandwidth, RAM, an CPU resources are limited and if your hosting provider does not provide a DOS/DDOS protection.

The following changes in the configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) will allow this and make it possible to proxy the federation through a CDN such as CloudFlare or any other:

```
matrix_synapse_http_listener_resource_names: ["client","federation"]
# Any port can be used but in this case we use 443
matrix_federation_public_port: 443
matrix_synapse_federation_port_enabled: false
# Note that the following change might not be "required per se" but probably will be due to the proxying of the traffic through the CDN proxy servers (CloudFlare for instance). The security impact of doing this should be minimal as your CDN itself will encrypt the traffic no matter what on their proxy servers. You could however first try and see if federation works while setting the following to true.
matrix_synapse_tls_federation_listener_enabled: false
```

**Use this at you own risk as all the possible side-effects of doing this are not fully known. However, it has been tested and works fine and passes all the tests on <https://federationtester.matrix.org/> without issues.**
