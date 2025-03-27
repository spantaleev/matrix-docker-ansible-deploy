<!--
SPDX-FileCopyrightText: 2018 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2021 Agustin Ferrario
SPDX-FileCopyrightText: 2020 Eneko Nieto
SPDX-FileCopyrightText: 2020 Julian Foad
SPDX-FileCopyrightText: 2020 Tomas Strand
SPDX-FileCopyrightText: 2021 Aaron Raimist
SPDX-FileCopyrightText: 2021 Colin Shea
SPDX-FileCopyrightText: 2022 François Darveau
SPDX-FileCopyrightText: 2022 Jaden Down
SPDX-FileCopyrightText: 2023 - 2024 Jost Alemann
SPDX-FileCopyrightText: 2023 Tilo Spannagel
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Using your own webserver, instead of this playbook's Traefik reverse-proxy (optional, advanced)

By default, this playbook installs its own [Traefik](https://traefik.io/) reverse-proxy server (in a Docker container) which listens on ports 80 and 443. If that's okay, you can skip this document.

## Traefik

[Traefik](https://traefik.io/) is the default reverse-proxy for the playbook since [2023-02-26](../CHANGELOG.md/#2023-02-26) and serves **2 purposes**:

- serving public traffic and providing SSL-termination with certificates obtained from [Let's Encrypt](https://letsencrypt.org/). See [Adjusting SSL certificate retrieval](./configuring-playbook-ssl-certificates.md).

- assists internal communication between addon services (bridges, bots, etc.) and the homeserver via an internal entrypoint (`matrix-internal-matrix-client-api`).

There are 2 ways to use Traefik with this playbook, as described below.

### Traefik managed by the playbook

To have the playbook install and use Traefik, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik
```

Traefik will manage SSL certificates for all services seamlessly.

### Traefik managed by you

```yaml
matrix_playbook_reverse_proxy_type: other-traefik-container

# Uncomment and adjust this part if your Traefik container is on another network
# matrix_playbook_reverse_proxy_container_network: traefik

# Adjust to point to your Traefik container
matrix_playbook_reverse_proxy_hostname: name-of-your-traefik-container

traefik_certs_dumper_ssl_dir_path: "/path/to/your/traefiks/acme.json/directory"

# Uncomment and adjust the variable below if the name of your federation entrypoint is different
# than the default value (matrix-federation).
# matrix_federation_traefik_entrypoint_name: matrix-federation

# Uncomment and adjust the variables below if you'd like to enable HTTP-compression.
#
# For this to work, you will need to define a compress middleware (https://doc.traefik.io/traefik/middlewares/http/compress/) for your Traefik instance
# using a file (https://doc.traefik.io/traefik/providers/file/) or Docker (https://doc.traefik.io/traefik/providers/docker/) configuration provider.
#
# matrix_playbook_reverse_proxy_traefik_middleware_compression_enabled: true
# matrix_playbook_reverse_proxy_traefik_middleware_compression_name: my-compression-middleware@file
```

In this mode all roles will still have Traefik labels attached. You will, however, need to configure your Traefik instance and its entrypoints.

By default, the playbook configured a `default` certificate resolver and multiple entrypoints.

You need to configure 4 entrypoints for your Traefik server:

- `web` (TCP port `80`) — used for redirecting to HTTPS (`web-secure`)
- `web-secure` (TCP port `443`) — used for exposing the Matrix Client-Server API and all other services
- `matrix-federation` (TCP port `8448`) — used for exposing the Matrix Federation API
- `matrix-internal-matrix-client-api` (TCP port `8008`) — used internally for addon services (bridges, bots) to communicate with the homserver

Below is some configuration for running Traefik yourself, although we recommend using [Traefik managed by the playbook](#traefik-managed-by-the-playbook).

Note that this configuration on its own does **not** redirect traffic on port 80 (plain HTTP) to port 443 for HTTPS. If you are not already doing this in Traefik, it can be added to Traefik in a [file provider](https://docs.traefik.io/v2.0/providers/file/) as follows:

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
    image: "docker.io/traefik:v3.2.0"
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
      - "--entrypoints.matrix-federation.address=:8448"
      - "--entrypoints.matrix-internal-matrix-client-api.address=:8008"
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

If you don't wish to use Traefik, you can also use your own webserver.

Doing this is possible, but requires manual work.

There are 2 ways to go about it:

- (recommended) [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) — using the playbook-managed reverse-proxy (Traefik), but disabling SSL termination for it, exposing this reverse-proxy on a few local ports (e.g. `127.0.0.1:81`, etc.) and forwarding traffic from your own webserver to those few ports

- (difficult) [Using no reverse-proxy on the Matrix side at all](#using-no-reverse-proxy-on-the-matrix-side-at-all) disabling the playbook-managed reverse-proxy (Traefik), exposing services one by one using `_host_bind_port` variables and forwarding traffic from your own webserver to those ports

### Fronting the integrated reverse-proxy webserver with another reverse-proxy

This method is about leaving the integrated reverse-proxy webserver be, but making it not get in the way (using up important ports, trying to retrieve SSL certificates, etc.).

If you wish to use another webserver, the integrated reverse-proxy webserver usually gets in the way because it attempts to fetch SSL certificates and binds to ports 80, 443 and 8448 (if Matrix Federation is enabled).

You can disable such behavior and make the integrated reverse-proxy webserver only serve traffic locally on the host itself (or over a local network).

This is the recommended way for using another reverse-proxy, because the integrated one would act as a black box and wire all Matrix services correctly. You would then only need to reverse-proxy a few individual domains and ports over to it.

To front Traefik with another reverse-proxy, you would need some configuration like this:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik

# Ensure that public urls use https
matrix_playbook_ssl_enabled: true

# Disable the web-secure (port 443) endpoint, which also disables SSL certificate retrieval.
# This has the side-effect of also automatically disabling TLS for the matrix-federation entrypoint
# (by toggling `matrix_federation_traefik_entrypoint_tls`).
traefik_config_entrypoint_web_secure_enabled: false

# If your reverse-proxy runs on another machine, consider using `0.0.0.0:81`, just `81` or `SOME_IP_ADDRESS_OF_THIS_MACHINE:81`
traefik_container_web_host_bind_port: '127.0.0.1:81'

# We bind to `127.0.0.1` by default (see above), so trusting `X-Forwarded-*` headers from
# a reverse-proxy running on the local machine is safe enough.
# If you're publishing the port (`traefik_container_web_host_bind_port` above) to a public network interface:
# - remove the `traefik_config_entrypoint_web_forwardedHeaders_insecure` variable definition below
# - uncomment and adjust the `traefik_config_entrypoint_web_forwardedHeaders_trustedIPs` line below
traefik_config_entrypoint_web_forwardedHeaders_insecure: true
# traefik_config_entrypoint_web_forwardedHeaders_trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']

# Expose the federation entrypoint on a custom port (other than port 8448, which is normally used publicly).
#
# We bind to `127.0.0.1` by default (see above), so trusting `X-Forwarded-*` headers from
# a reverse-proxy running on the local machine is safe enough.
#
# If your reverse-proxy runs on another machine, consider:
# - using `0.0.0.0:8449`, just `8449` or `SOME_IP_ADDRESS_OF_THIS_MACHINE:8449` below
# - adjusting `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_custom` (below) - removing `insecure: true` and enabling/configuring `trustedIPs`
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port: '127.0.0.1:8449'

# Disable HTTP/3 for the federation entrypoint.
# If you'd like HTTP/3, consider configuring it for your other reverse-proxy.
#
# Disabling this also sets `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port_udp` to an empty value.
# If you'd like to keep HTTP/3 enabled here (for whatever reason), you may wish to explicitly
# set `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port_udp` to something like '127.0.0.1:8449'.
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_http3_enabled: false

# Depending on the value of `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port` above,
# this may need to be reconfigured. See the comments above.
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_custom:
  forwardedHeaders:
    insecure: true
  # trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']
```

Such a configuration would expose all services on a local port `81` and Matrix Federation on a local port `8449`. Your reverse-proxy configuration needs to send traffic to these ports. [`examples/reverse-proxies`](../examples/reverse-proxies/) contains examples for various webservers such as Apache2, Caddy, HAproxy, nginx and Nginx Proxy Manager.

It's important that these webservers proxy-pass requests to the correct `ip:port` and also set the `Host` HTTP header appropriately. If you don't pass the `Host` header correctly, Traefik will return a `404 - not found` error.

To put it another way:
- `curl http://127.0.0.1:81` will result in a `404 - not found` error
- but `curl -H 'Host: matrix.example.com' http://127.0.0.1:81` should work.

### Using no reverse-proxy on the Matrix side at all

Instead of [Fronting the integrated reverse-proxy webserver with another reverse-proxy](#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy), you can also go another way — completely disabling the playbook-managed Traefik reverse-proxy. You would then need to reverse-proxy from your own webserver directly to each individual Matrix service.

This is more difficult, as you would need to handle the configuration for each service manually. Enabling additional services would come with extra manual work you need to do.

Also, the Traefik reverse-proxy, besides fronting everything is also serving a 2nd purpose of allowing addons services to communicate with the Matrix homeserver thanks to its `matrix-internal-matrix-client-api` entrypoint (read more about it above). Disabling Traefik completely means the playbook would wire services to directly talk to the homeserver. This can work for basic setups, but not for more complex setups involving [matrix-media-repo](./configuring-playbook-matrix-media-repo.md), [matrix-corporal](./configuring-playbook-matrix-corporal.md) or other such services that need to "steal routes" from the homeserver.

If your webserver is on the same machine, ensure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`. This allows your webserver user to access files owned by the `matrix` group, so that it can serve static files from `/matrix/static-files`.
