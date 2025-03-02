<!--
SPDX-FileCopyrightText: 2023 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 Jost Alemann
SPDX-FileCopyrightText: 2024 Rubén Cabrera
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Nginx reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to use the [nginx](https://nginx.org/) webserver to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with another reverse-proxy.

## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.example.com/vars.yml`).

## Using the nginx configuration

Copy the [matrix.conf](matrix.conf) file to your nginx server's filesystem, modify it to your needs and include it in your nginx configuration (e.g. `include /path/to/matrix.conf;`).

This configuration **disables SSL certificate retrieval**, so you will **need to obtain SSL certificates manually** (e.g. by using [certbot](https://certbot.eff.org/)) and set the appropriate path in `matrix.conf`. In the example nginx configuration, a single certificate is used for all subdomains (`matrix.example.com`, `element.example.com`, etc.). For your setup, may wish to change this and use separate `server` blocks and separate certificate files for each host.

Also note that your copy of the `matrix.conf` file has to be adapted to whatever services you are using. For example, remove `element.example.com` from the `server_name` list if you don't use [Element Web](../../../docs/configuring-playbook-client-element-web.md) client or add `dimension.example.com` to it if you do use the [Dimension](../../../docs/configuring-playbook-dimension.md) integration manager.
