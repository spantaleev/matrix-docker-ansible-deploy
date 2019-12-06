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

1) Make sure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`

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
matrix_nginx_proxy_ssl_protocols: "TLSv1.1 TLSv1.2"
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
The expected domains vary depending on the services you have enabled (`matrix.DOMAIN` for sure; `riot.DOMAIN` and `dimension.DOMAIN` are optional).

We don't have sample webserver configuration for this use-case yet, but hope to expand on this documentation entry in the future.
For [Traefik](https://traefik.io/), you can [see some work in progress examples here](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/296).
