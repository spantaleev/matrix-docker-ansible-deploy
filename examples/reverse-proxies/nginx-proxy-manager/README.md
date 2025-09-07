<!--
SPDX-FileCopyrightText: 2024 Gouthaman Raveendran
SPDX-FileCopyrightText: 2024 MDAD project contributors
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
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

Again, under the 'Proxy Hosts' page select `Add Proxy Host`, this time for your federation traffic. Apply the proxy's configuration like this:

```md
# Details
# Matrix Federation proxy config
Domain Names: matrix.example.com:8448
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 8449

# SSL
# Either 'Request a new certificate' or select an existing one
SSL Certificate: matrix.example.com or *.example.com
Force SSL: true
HTTP/2 Support: true

# Advanced
# Allows NPM to listen on the federation port
Custom Nginx Configuration:
	listen 8448 ssl http2;
	client_max_body_size 50M;
```

Also note, NPM would need to be configured for whatever other services you are using. For example, you would need to create additional proxy hosts for `element.example.com` or `jitsi.example.com`, which would use the forwarding port `81`.
