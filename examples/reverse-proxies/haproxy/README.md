# HAproxy reverse-proxy

This directory contains sample files that show you how to do reverse-proxying using HAproxy.

This is for when you wish to have your own HAproxy instance sitting in front of Matrix services installed by this playbook.

We recommend that you use HAProxy in front of Traefik. See our [Fronting the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) documentation.

You can then use the configuration files from this directory as an example for how to configure your HAproxy reverse proxy.
