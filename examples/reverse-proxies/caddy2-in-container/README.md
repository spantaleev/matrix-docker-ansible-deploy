<!--
SPDX-FileCopyrightText: 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Caddy reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with your own **containerized** [Caddy](https://caddyserver.com/) reverse-proxy. If you have a server with a Caddy container already serving several applications and you want to install Matrix on it (with no changes to existing traffic routing), then this guide is for you.

**Note**: if you're running Caddy on the host itself (not in a container), refer to the [caddy2](../caddy2/README.md) example instead.

## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.example.com/vars.yml`).

Then, adjust your Caddy  `docker-compose.yaml` file (if you're using docker-compose for running your Caddy container). See [examples/reverse-proxies/caddy2-in-container/docker-compose.yaml](./docker-compose.yaml).

## Using the Caddyfile

You can either just use the [Caddyfile](Caddyfile) directly or append its content to your own Caddyfile.
In both cases make sure to replace all the `example.com` domains with your own domain.

This example does not include additional services like Element Web, but you should be able copy the first block and replace the `matrix.` subdomain with the subdomain of the some other service (e.g. `element.`).
