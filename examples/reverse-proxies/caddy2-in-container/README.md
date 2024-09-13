# Caddy reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with your own container-ed  [Caddy](https://caddyserver.com/) reverse-proxy. If you have a server with a Caddy container already serving several applications. And you want to install Matrix on it, but you don't want to break the existing traffic routing (so that the existing applications keep running smoothly). Then this guide is helpful.

Note: if you're running Caddy on the host itself (not in a container), refer to the [caddy2](../caddy2/README.md) example instead.


## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`).

And adjust the `docker-compose.yaml` of Caddy's. See [examples/reverse-proxies/caddy2-in-container/docker-compose.yaml](./docker-compose.yaml).


## Using the Caddyfile

You can either just use the [Caddyfile](Caddyfile) directly or append its content to your own Caddyfile.
In both cases make sure to replace all the `example.tld` domains with your own domain.

This example does not include additional services like Element, but you should be able copy the first block and replace the `matrix.` subdomain with the subdomain of the some other service (e.g. `element.`).
