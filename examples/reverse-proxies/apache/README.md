<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Rubén Cabrera
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Apache reverse-proxy

This directory contains sample files that show you how to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with your Apache reverse-proxy.

## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.example.com/vars.yml`).

## Using the Apache configuration

`matrix-domain.conf` contains configuration for the Matrix domain, which handles both the Client-Server API (port `443`) and the Matrix Federation API (port `8448`).

`matrix-client-element.conf` is an example for when you're hosting Element Web at `element.example.com`.
This configuration can also be used as an example for handling other domains, depending on the services you enable with the playbook (e.g. `dimension.example.com`, etc).
