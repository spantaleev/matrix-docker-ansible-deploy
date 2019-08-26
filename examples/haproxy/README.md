# HAproxy reverse-proxy

This directory contains sample files that show you how to do reverse-proxying using HAproxy.

This is for when you wish to have your own HAproxy instance sitting in front of Matrix services installed by this playbook.
See the [Using your own webserver, instead of this playbook's nginx proxy](../../docs/configuring-playbook-own-webserver.md) documentation page.

To use your own HAproxy reverse-proxy, you first need to disable the integrated Nginx server.
You do that with the following custom configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_nginx_proxy_enabled: false
```

You can then use the configuration files from this directory as an example for how to configure your HAproxy reverse proxy.

**NOTE**: this is just an example and may not be entirely accurate. It may also not cover other use cases or performance needs.

### Configuration

HAproxy, unlike Apache, Nginx and others, does not provide you with a webserver to serve static files (i.e., `/.well-known/` directory). For this reason, in this folder you can find an example on how to use HAproxy together with a simple Nginx container whose only task is to serve those files.

* Build the Docker image. `docker build -t local/nginx .` 
* Start the container. `docker-compose up -d`. Note that if you want to run Nginx on a different port, you will have to change the port both in the `docker-compose.yml` and in `haproxy.cfg`.
* If you don't want to use a wildcard certificate, you will need to modify the corresponding line in the HTTPS frontent and add the paths of all the specific certificates (as for the commented example in `haproxy.cfg`).
* Start HAproxy with the proposed configuration.
