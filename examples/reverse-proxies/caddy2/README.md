<!--
SPDX-FileCopyrightText: 2020 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2021 Rafael Girão
SPDX-FileCopyrightText: 2024 Rubén Cabrera
SPDX-FileCopyrightText: 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Caddy reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with your own [Caddy](https://caddyserver.com/) reverse-proxy.

## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.example.com/vars.yml`).

## Using the Caddyfile

You can either just use the [Caddyfile](Caddyfile) directly or append its content to your own Caddyfile.
In both cases make sure to replace all the `example.com` domains with your own domain.

This example does not include additional services like Element, but you should be able copy the first block and replace the `matrix` subdomain with the additional services subdomain. I have not tested this though.
