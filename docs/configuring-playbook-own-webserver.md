# Using your own webserver, instead of this playbook's Traefik reverse-proxy (optional, advanced)

**Note**: the playbook is [in the process of moving to Traefik](../CHANGELOG.md#reverse-proxy-configuration-changes-and-initial-traefik-support). The **documentation below may be incomplete or misleading**.

By default, this playbook installs its own nginx webserver (called `matrix-nginx-proxy`, in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.

Soon, this default will change and the playbook will install its own [Traefik](https://traefik.io/) reverse-proxy instead.

## Traefik

[Traefik](https://traefik.io/) will be the default reverse-proxy for the playbook in the near future.

There are 2 ways to use Traefik with this playbook, as described below.

### Traefik managed by the playbook

To switch to Traefik now, use configuration like this:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik

devture_traefik_config_certificatesResolvers_acme_email: YOUR_EMAIL_ADDRESS
```

This will install Traefik in the place of `matrix-nginx-proxy`. Traefik will manage SSL certificates for all services seamlessly.

**Note**: during the transition period, `matrix-nginx-proxy` will still be installed in local-only mode. Do not be alarmed to see `matrix-nginx-proxy` running even when you've chosen Traefik as your reverse-proxy. In the future, we'll be able to run without nginx, but we're not there yet.

### Traefik managed by you

```yaml
matrix_playbook_reverse_proxy_type: other-traefik-container

matrix_playbook_reverse_proxyable_services_additional_network: your-traefik-network

devture_traefik_certs_dumper_ssl_dir_path: "/path/to/your/traefiks/acme.json/directory"
```

In this mode all roles will still have Traefik labels attached. You will, however, need to configure your Traefik instance and its entrypoints.

By default, the playbook congiures services use a `web-secure` (443) and `matrix-federation` (8448) entrypoints, as well as a `default` certificate resolver.

You need to configure 3 entrypoints for your Traefik server: `web` (TCP port `80`), `web-secure` (TCP port `443`) and `matrix-federation` (TCP port `8448`).

Below is some configuration for running Traefik yourself, although we recommend using [Traefik managed by the playbook](#traefik-managed-by-the-playbook).

Note that this configuration on its own does **not** redirect traffic on port 80 (plain HTTP) to port 443 for HTTPS, which may cause some issues, since the built-in Nginx proxy usually does this. If you are not already doing this in Traefik, it can be added to Traefik in a [file provider](https://docs.traefik.io/v2.0/providers/file/) as follows:

```toml
[http]
  [http.routers]
    [http.routers.redirect-http]
      entrypoints = ["web"] # The 'web' entrypoint must bind to port 80
      rule = "HostRegexp(`{host:.+}`)" # Change if you don't want to redirect all hosts to HTTPS
      service = "dummy" # Unused, but all routers need services (for now)
      middlewares = ["https"]
  [http.services]
    [http.services.dummy.loadbalancer]
      [[http.services.dummy.loadbalancer.servers]]
        url = "localhost"
  [http.middlewares]
    [http.middlewares.https.redirectscheme]
      scheme = "https"
      permanent = true
```

You can use the following `docker-compose.yml` as example to launch Traefik.

```yaml
version: "3.3"

services:

  traefik:
    image: "docker.io/traefik:v2.9.6"
    restart: always
    container_name: "traefik"
    networks:
      - traefik
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.network=traefik"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web-secure.address=:443"
      - "--entrypoints.federation.address=:8448"
      - "--certificatesresolvers.default.acme.tlschallenge=true"
      - "--certificatesresolvers.default.acme.email=YOUR EMAIL"
      - "--certificatesresolvers.default.acme.storage=/letsencrypt/acme.json"
    ports:
      - "443:443"
      - "8448:8448"
    volumes:
      - "./letsencrypt:/letsencrypt"
      - "/var/run/docker.sock:/var/run/docker.sock:ro"

networks:
  traefik:
    external: true
```

## Another webserver

If you don't wish to use Traefik or `matrix-nginx-proxy`, you can also use your own webserver.

Doing this is possible, but requires manual work.

There are 2 ways to go about it:

- (recommended) [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) - using a playbook-managed reverse-proxy (either `matrix-nginx-proxy` or Traefik), disabling SSL termination for it, exposing this reverse-proxy on a few local ports (e.g. `127.0.0.1:81`, etc.) and forwarding traffic from your own webserver to those few ports

- (difficult) [Using no reverse-proxy on the Matrix side at all](#using-no-reverse-proxy-on-the-matrix-side-at-all) disabling all playbook-managed reverse-proxies (no `matrix-nginx-proxy`, no Traefik)


### Fronting the integrated reverse-proxy webserver with another reverse-proxy

This method is about leaving the integrated reverse-proxy webserver be, but making it not get in the way (using up important ports, trying to retrieve SSL certificates, etc.).

If you wish to use another webserver, the integrated reverse-proxy webserver usually gets in the way because it attempts to fetch SSL certificates and binds to ports 80, 443 and 8448 (if Matrix Federation is enabled).

You can disable such behavior and make the integrated reverse-proxy webserver only serve traffic locally (or over a local network).

This is the recommended way for using another reverse-proxy, because the integrated one would act as a black box and wire all Matrix services correctly. You would only need to reverse-proxy a few individual domains and ports over to it.

To front Traefik with another reverse-proxy, you would need some configuration like this:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik

# Ensure that public urls use https
matrix_playbook_ssl_enabled: true

# Disable the web-secure (port 443) endpoint, which also disables SSL certificate retrieval
devture_traefik_config_entrypoint_web_secure_enabled: false

# If your reverse-proxy runs on another machine, consider using `0.0.0.0:81`, just `81` or `SOME_IP_ADDRESS_OF_THIS_MACHINE:81`
devture_traefik_container_web_host_bind_port: '127.0.0.1:81'

# We bind to `127.0.0.1` by default (see above), so trusting `X-Forwarded-*` headers from
# a reverse-proxy running on the local machine is safe enough.
devture_traefik_config_entrypoint_web_forwardedHeaders_insecure: true

# Or, if you're publishing the port (`devture_traefik_container_web_host_bind_port` above) to a public network interfaces:
# - remove the `devture_traefik_config_entrypoint_web_forwardedHeaders_insecure` variable definition above
# - uncomment and adjust the line below
# devture_traefik_config_entrypoint_web_forwardedHeaders_trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']

# Likewise (to `devture_traefik_container_web_host_bind_port` above),
# if your reverse-proxy runs on another machine, consider changing the `host_bind_port` setting below.
devture_traefik_additional_entrypoints_auto:
  - name: matrix-federation
    port: 8449
    host_bind_port: '127.0.0.1:8449'
    config: {}
    # If your reverse-proxy runs on another machine, remove the config above and use this config instead:
    # config:
    #   forwardedHeaders:
    #     insecure: true
    #     # trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']
```

For an example where the playbook's Traefik reverse-proxy is fronted by another reverse-proxy running on the same server, see [Nginx reverse-proxy fronting the playbook's Traefik](../examples/nginx/README.md) or [Caddy reverse-proxy fronting the playbook's Traefik](../examples/caddy2/README.md).


### Using no reverse-proxy on the Matrix side at all

Instead of [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy), you can also go another way -- completely disabling the playbook-managed reverse-proxy. You would then need to reverse-proxy from your own webserver directly to Matrix services.

This is more difficult, as you would need to handle the configuration for each service manually. Enabling additional services would come with extra manual work you need to do.

If your webserver is on the same machine, sure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`. This allows your webserver user to access files owned by the `matrix` group. When using an external nginx webserver, this allows it to read configuration files from `/matrix/nginx-proxy/conf.d`. When using another server, it would make other files, such as `/matrix/static-files/.well-known`, accessible to it.

#### Using your own nginx reverse-proxy running on the same machine

**WARNING**: this type of setup is not maintained and will be removed in the future. We recommend that you go for [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instead.

If you'll be using `nginx` running on the same machine (not in a container), you can make the playbook help you generate configuration for `nginx` with this configuration:

```yaml
matrix_playbook_reverse_proxy_type: other-nginx-non-container

# If you want https configured in /matrix/nginx-proxy/conf.d/
matrix_nginx_proxy_https_enabled: true

# If you will manage SSL certificates yourself, uncomment the line below
# matrix_ssl_retrieval_method: none

# If you're using an old nginx version, consider using a custom protocol list
# (removing `TLSv1.3` that is enabled by default) to suit your nginx version.
# matrix_nginx_proxy_ssl_protocols: "TLSv1.2"
```

You can most likely directly use the config files installed by this playbook at: `/matrix/nginx-proxy/conf.d`. Just include them in your own `nginx.conf` like this: `include /matrix/nginx-proxy/conf.d/*.conf;`

#### Using your own reverse-proxy running on the same machine or elsewhere

**WARNING**: this is difficult to set up, likely not very well supported and will be removed in the future. We recommend that you go for [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instead.

To reverse-proxy manually for each service, use configuration like this:

```yaml
# If your reverse-proxy runs on the same machine:
matrix_playbook_reverse_proxy_type: other-on-same-host

# Or, if it runs on another machine:
# matrix_playbook_reverse_proxy_type: other-on-another-host

# Or, optionally customize the network interface prefix (note the trailing `:` character).
# For other-on-same-host, the interface defaults to `127.0.0.1:`.
# For other-on-another-host, the interface defaults to `0.0.0.0:`.
# matrix_playbook_service_host_bind_interface_prefix: '192.168.30.4:'
```

With this configuration, each service will be exposed on a custom port. Example:

- Synapse will be exposed on port `8008`
- [Grafana](configuring-playbook-prometheus-grafana.md) will be exposed on port `3000`
- [synapse-admin](configuring-playbook-synapse-admin.md) will be exposed on port `8766`

You can capture traffic for these services and forward it to their port.
Some of these services are configured with certain default expecations with regard to hostname, path, etc., so it's not completely arbitrary where you can host them (unless you change the defaults).

For each new playbook service that you enable, you'll need special handling.

The [`examples/`](../examples/) directory contains examples for various servers: Caddy, Apache, HAproxy, Nginx, etc.
