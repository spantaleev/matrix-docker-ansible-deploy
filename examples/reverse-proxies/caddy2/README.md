# Caddy reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with your own [Caddy](https://caddyserver.com/) reverse-proxy.


## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`).


## Using the Caddyfile

You can either just use the [Caddyfile](Caddyfile) directly or append its content to your own Caddyfile.
In both cases make sure to replace all the `example.tld` domains with your own domain.

This example does not include additional services like element, but you should be able copy the first block and replace the matrix subdomain with the additional services subdomain. I have not tested this though.
