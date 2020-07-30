# Serving the base domain

This playbook sets up services on your Matrix server (`matrix.DOMAIN`).
To have this server officially be responsible for Matrix services for the base domain (`DOMAIN`), you need to set up [Server Delegation](howto-server-delegation.md).
This is normally done by [configuring well-known](configuring-well-known.md) files on the base domain.

People who don't have a separate server to dedicate to the base domain have trouble arranging this.

Usually, there are 2 options:

- either get a separate server for the base domain, just for serving the files necessary for [Server Delegation via a well-known file](howto-server-delegation.md#server-delegation-via-a-well-known-file)

- or, arrange for the Matrix server to serve the base domain. This either involves you [using your own webserver](configuring-playbook-own-webserver.md) or making the integrated webserver (`matrix-nginx-proxy`) serve the base domain for you.

This documentation page tells you how to do the latter. With some easy changes, we make it possible to serve the base domain from the Matrix server via the integrated webserver (`matrix-nginx-proxy`).

Just **adjust your DNS records**, so that your base domain is pointed to the Matrix server's IP address (using a DNS `A` record) **and then use the following configuration**:

```yaml
matrix_nginx_proxy_base_domain_serving_enabled: true
```

Doing this, the playbook will:

- obtain an SSL certificate for the base domain, just like it does for all other domains (see [how we handle SSL certificates](configuring-playbook-ssl-certificates.md))

- serve the `/.well-known/matrix/*` files which are necessary for [Federation Server Discovery](configuring-well-known.md#introduction-to-client-server-discovery) (also see [Server Delegation](howto-server-delegation.md)) and [Client-Server discovery](configuring-well-known.md#introduction-to-client-server-discovery)

- serve a simple homepage at `https://DOMAIN` with content `Hello from DOMAIN` (configurable via the `matrix_nginx_proxy_base_domain_homepage_template` variable). You can also [serve a more complicated static website](#serving-a-static-website-at-the-base-domain).


## Serving a static website at the base domain

By default, when "serving the base domain" is enabled, the playbook hosts a simple `index.html` webpage in `/matrix/nginx-proxy/data/matrix-domain`.
The content of this page is taken from the `matrix_nginx_proxy_base_domain_homepage_template` variable.

If you'd like to host your own static website (more than a single `index.html` page) at the base domain, you can disable the creation of this default `index.html` page like this:

```yaml
matrix_nginx_proxy_base_domain_homepage_enabled: false
```

With this configuration, Ansible will no longer mess around with the `/matrix/nginx-proxy/data/matrix-domain/index.html` file.

You are then free to upload any static website files to `/matrix/nginx-proxy/data/matrix-domain` and they will get served at the base domain.


## Serving a more complicated website at the base domain

If you'd like to serve an even more complicated (dynamic) website from the Matrix server, relying on the playbook to serve the base domain is not the best choice.

Instead, we recommend that you switch to [using your own webserver](configuring-playbook-own-webserver.md) (preferrably nginx). You can then make that webserver host anything you wish, and still easily plug in Matrix services into it.
