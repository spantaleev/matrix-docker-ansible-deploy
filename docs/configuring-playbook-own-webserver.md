# Using your own webserver, instead of this playbook's nginx proxy (optional, advanced)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.

If you don't want this playbook's nginx webserver to take over your server's 80/443 ports like that,
and you'd like to use your own webserver (be it nginx, Apache, Varnish Cache, etc.), you can.

There are **2 ways you can go about it**, if you'd like to use your own webserver:

- [Method 1: Disabling the integrated nginx reverse-proxy webserver](#method-1-disabling-the-integrated-nginx-reverse-proxy-webserver)

- [Method 2: Fronting the integrated nginx reverse-proxy webserver with another reverse-proxy](#method-2-fronting-the-integrated-nginx-reverse-proxy-webserver-with-another-reverse-proxy)


## Method 1: Disabling the integrated nginx reverse-proxy webserver

This method is about completely disabling the integrated nginx reverse-proxy webserver and replicating its behavior using another webserver.
For an alternative, make sure to check Method #2 as well.

### Preparation

No matter which external webserver you decide to go with, you'll need to:

1) Make sure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`. This allows your webserver user to access files owned by the `matrix` group. When using an external nginx webserver, this allows it to read configuration files from `/matrix/nginx-proxy/conf.d`. When using another server, it would make other files, such as `/matrix/static-files/.well-known`, accessible to it.

2) Edit your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) to disable the integrated nginx server:

```yaml
matrix_nginx_proxy_enabled: false
```

3) **If you'll manage SSL certificates by yourself**, edit your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) to disable SSL certificate retrieval:

```yaml
matrix_ssl_retrieval_method: none
```

**Note**: During [installation](installing.md), unless you've disabled SSL certificate management (`matrix_ssl_retrieval_method: none`), the playbook would need 80 to be available, in order to retrieve SSL certificates. **Please manually stop your other webserver while installing**. You can start it back up afterwards.


### Using your own external nginx webserver

Once you've followed the [Preparation](#preparation) guide above, it's time to set up your external nginx server.

Even with `matrix_nginx_proxy_enabled: false`, the playbook still generates some helpful files for you in `/matrix/nginx-proxy/conf.d`.
Those configuration files are adapted for use with an external web server (one not running in the container network).

You can most likely directly use the config files installed by this playbook at: `/matrix/nginx-proxy/conf.d`. Just include them in your own `nginx.conf` like this: `include /matrix/nginx-proxy/conf.d/*.conf;`

Note that if your nginx version is old, it might not like our default choice of SSL protocols (particularly the fact that the brand new `TLSv1.3` protocol is enabled). You can override the protocol list by redefining the `matrix_nginx_proxy_ssl_protocols` variable. Example:

```yaml
# Custom protocol list (removing `TLSv1.3`) to suit your nginx version.
matrix_nginx_proxy_ssl_protocols: "TLSv1.2"
```


### Using your own external Apache webserver

Once you've followed the [Preparation](#preparation) guide above, you can take a look at the [examples/apache](../examples/apache) directory for a sample configuration.

### Using your own external caddy webserver

After following  the [Preparation](#preparation) guide above, you can take a look at the [examples/caddy](../examples/caddy) directory for a sample configuration.

### Using your own HAproxy reverse proxy
After following  the [Preparation](#preparation) guide above, you can take a look at the [examples/haproxy](../examples/haproxy) directory for a sample configuration. In this case HAproxy is used as a reverse proxy and a simple Nginx container is used to serve statically `.well-known` files.

### Using another external webserver

Feel free to look at the [examples/apache](../examples/apache) directory, or the [template files in the matrix-nginx-proxy role](../roles/matrix-nginx-proxy/templates/conf.d/).


## Method 2: Fronting the integrated nginx reverse-proxy webserver with another reverse-proxy

This method is about leaving the integrated nginx reverse-proxy webserver be, but making it not get in the way (using up important ports, trying to retrieve SSL certificates, etc.).

If you wish to use another webserver, the integrated nginx reverse-proxy webserver usually gets in the way because it attempts to fetch SSL certificates and binds to ports 80, 443 and 8448 (if Matrix Federation is enabled).

You can disable such behavior and make the integrated nginx reverse-proxy webserver only serve traffic locally (or over a local network).

You would need some configuration like this:

```yaml
# Do not retrieve SSL certificates. This shall be managed by another webserver or other means.
matrix_ssl_retrieval_method: none

# Do not try to serve HTTPS, since we have no SSL certificates.
# Disabling this also means services will be served on the HTTP port
# (`matrix_nginx_proxy_container_http_host_bind_port`).
matrix_nginx_proxy_https_enabled: false

# Do not listen for HTTP on port 80 globally (default), listen on the loopback interface.
# If you'd like, you can make it use the local network as well and reverse-proxy from another local machine.
matrix_nginx_proxy_container_http_host_bind_port: '127.0.0.1:81'

# Likewise, expose the Matrix Federation port on the loopback interface.
# Since `matrix_nginx_proxy_https_enabled` is set to `false`, this federation port will serve HTTP traffic.
# If you'd like, you can make it use the local network as well and reverse-proxy from another local machine.
#
# You'd most likely need to expose it publicly on port 8448 (8449 was chosen for the local port to prevent overlap).
matrix_nginx_proxy_container_federation_host_bind_port: '127.0.0.1:8449'

# Coturn relies on SSL certificates that have already been obtained.
# Since we don't obtain any certificates (`matrix_ssl_retrieval_method: none` above), it won't work by default.
# An alternative is to tweak some of: `matrix_coturn_tls_enabled`, `matrix_coturn_tls_cert_path` and `matrix_coturn_tls_key_path`.
matrix_coturn_enabled: false
```

With this, nginx would still be in use, but it would not bother with anything SSL related or with taking up public ports.

All services would be served locally on `127.0.0.1:81` and `127.0.0.1:8449` (as per the example configuration above).

You can then set up another reverse-proxy server on ports 80/443/8448 for all of the expected domains and make traffic go to these local ports.
The expected domains vary depending on the services you have enabled (`matrix.DOMAIN` for sure; `element.DOMAIN`, `dimension.DOMAIN` and `jitsi.DOMAIN` are optional).

### Sample configuration for running behind Traefik 2.0

Below is a sample configuration for using this playbook with a [Traefik](https://traefik.io/) 2.0 reverse proxy.

```yaml
# Disable generation and retrieval of SSL certs
matrix_ssl_retrieval_method: none

# Configure Nginx to only use plain HTTP
matrix_nginx_proxy_https_enabled: false

# Don't bind any HTTP or federation port to the host
# (Traefik will proxy directly into the containers)
matrix_nginx_proxy_container_http_host_bind_port: ''
matrix_nginx_proxy_container_federation_host_bind_port: ''

# Disable Coturn because it needs SSL certs
# (Clients can, though exposing IP address, use Matrix.org TURN)
matrix_coturn_enabled: false

# All containers need to be on the same Docker network as Traefik
# (This network should already exist and Traefik should be using this network)
matrix_docker_network: 'traefik'

matrix_nginx_proxy_container_extra_arguments:
  # May be unnecessary depending on Traefik config, but can't hurt
  - '--label "traefik.enable=true"'

  # The Nginx proxy container will receive traffic from these subdomains
  - '--label "traefik.http.routers.matrix-nginx-proxy.rule=Host(`{{ matrix_server_fqn_matrix }}`,`{{ matrix_server_fqn_element }}`,`{{ matrix_server_fqn_dimension }}`,`{{ matrix_server_fqn_jitsi }}`)"'

  # (The 'web-secure' entrypoint must bind to port 443 in Traefik config)
  - '--label "traefik.http.routers.matrix-nginx-proxy.entrypoints=web-secure"'

  # (The 'default' certificate resolver must be defined in Traefik config)
  - '--label "traefik.http.routers.matrix-nginx-proxy.tls.certResolver=default"'

  # The Nginx proxy container uses port 8080 internally
  - '--label "traefik.http.services.matrix-nginx-proxy.loadbalancer.server.port=8080"'

matrix_synapse_container_extra_arguments:
  # May be unnecessary depending on Traefik config, but can't hurt
  - '--label "traefik.enable=true"'

  # The Synapse container will receive traffic from this subdomain
  - '--label "traefik.http.routers.matrix-synapse.rule=Host(`{{ matrix_server_fqn_matrix }}`)"'

  # (The 'synapse' entrypoint must bind to port 8448 in Traefik config)
  - '--label "traefik.http.routers.matrix-synapse.entrypoints=synapse"'

  # (The 'default' certificate resolver must be defined in Traefik config)
  - '--label "traefik.http.routers.matrix-synapse.tls.certResolver=default"'

  # The Synapse container uses port 8048 internally
  - '--label "traefik.http.services.matrix-synapse.loadbalancer.server.port=8048"'
```

This method uses labels attached to the Nginx and Synapse containers to provide the Traefik Docker provider with the information it needs to proxy `matrix.DOMAIN`, `element.DOMAIN`, `dimension.DOMAIN` and `jitsi.DOMAIN`. Some [static configuration](https://docs.traefik.io/v2.0/reference/static-configuration/file/) is required in Traefik; namely, having endpoints on ports 443 and 8448 and having a certificate resolver.

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
    image: "traefik:v2.3"
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
      - "--entrypoints.synapse.address=:8448"
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
