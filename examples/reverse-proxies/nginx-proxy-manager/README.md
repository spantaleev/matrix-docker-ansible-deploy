<!--
SPDX-FileCopyrightText: 2024 Gouthaman Raveendran
SPDX-FileCopyrightText: 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2026 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nginx Proxy Manager fronting the playbook's integrated Traefik reverse-proxy

Similar to standard nginx, [Nginx Proxy Manager](https://nginxproxymanager.com/) provides nginx capabilities but inside a pre-built Docker container. With the ability for managing proxy hosts and automatic SSL certificates via a simple web interface.

This page summarizes how to use Nginx Proxy Manager (NPM) to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver.

## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.example.com/vars.yml`).

If Matrix federation is enabled, then you will need to make changes to [NPM's Docker configuration](https://nginxproxymanager.com/guide/#quick-setup). By default NPM already exposes ports `80` and `443`, but you would also need to **additionally expose the Matrix Federation port** (as it appears on the public side): `8448`.

## Using Nginx Proxy Manager

You'll need to create two proxy hosts in NPM for Matrix web and federation traffic.

Open the 'Proxy Hosts' page in the NPM web interface and select `Add Proxy Host`, the first being for Matrix web traffic. Apply the proxy's configuration like this:

```md
# Details
# Matrix web proxy config
Domain Names: matrix.example.com
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 81

# SSL
# Either 'Request a new certificate' or select an existing one
SSL Certificate: matrix.example.com or *.example.com
Force SSL: true
HTTP/2 Support: true

# Advanced
Custom Nginx Configuration:
	client_max_body_size 50M;
```

Then, under the 'Streams' page select `Add Stream`, this time for your federation traffic. Apply the configuration like this:

```md
# Details
# Matrix Federation proxy config
Incoming Port: 8448
Forward Host/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 8449
Protocols: TCP

# SSL
# Either 'Request a new certificate' or select an existing one
SSL Certificate: matrix.example.com or *.example.com
```

Also note, NPM would need to be configured for whatever other services you are using. For example, you would need to create additional proxy hosts for `element.example.com` or `jitsi.example.com`, which would use the forwarding port `81`.

## Serving the base domain (optional)

The configuration above only covers `matrix.example.com`. Many people serve their base domain (`example.com`) from somewhere else entirely, in which case there is nothing more to do here. Arrange [server delegation](../../../docs/howto-server-delegation.md) on whichever server hosts the base domain instead.

If you have made this Matrix server responsible for the base domain as well (by [serving the base domain](../../../docs/configuring-playbook-base-domain-serving.md) with `matrix_static_files_container_labels_base_domain_enabled: true`), then the base domain needs a proxy host of its own. Without it, requests for `https://example.com/.well-known/matrix/server` and `https://example.com/.well-known/matrix/client` never reach Traefik, NPM answers with a `404` error of its own, and both [Federation Server Discovery](../../../docs/configuring-well-known.md#federation-server-discovery) and [Client-Server discovery](../../../docs/configuring-well-known.md#client-server-discovery) break.

Add another proxy host, this time for the base domain:

```md
# Details
# Base domain proxy config
Domain Names: example.com
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 81

# SSL
# Note that a `*.example.com` wildcard certificate does not cover the base domain itself,
# so the certificate you use here needs to include `example.com`
SSL Certificate: example.com
Force SSL: true
HTTP/2 Support: true
```
