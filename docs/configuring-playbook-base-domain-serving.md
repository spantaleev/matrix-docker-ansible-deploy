<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Serving the base domain (optional)

By default, this playbook sets up services on your Matrix server (`matrix.example.com`), but has it configured so that it presents itself as the base domain (`example.com`). To have this server officially be responsible for Matrix services for the base domain (`example.com`), you need to set up server delegation / redirection.

As we discuss in [Server Delegation](howto-server-delegation.md), server delegation / redirection can be configured in either of these ways:

- Setting up a `/.well-known/matrix/server` file on the base domain (`example.com`)
- Setting up a `_matrix._tcp` DNS SRV record

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file.

However, those who don't have a separate server to dedicate to the base domain have trouble arranging this.

Usually, there are 2 options:

- either get a separate server for the base domain, just for serving the files necessary for [Server Delegation via a well-known file](howto-server-delegation.md#server-delegation-via-a-well-known-file)

- or, arrange for the Matrix server to serve the base domain. This either involves you [using your own webserver](configuring-playbook-own-webserver.md) or making the integrated webserver serve the base domain for you.

This documentation page tells you how to do the latter. With some easy changes, we make it possible to serve the base domain from the Matrix server via the integrated webserver.

Just [**adjust your DNS records**](configuring-dns.md), so that your base domain is pointed to the Matrix server's IP address (using a DNS `A` record) **and then add the following configuration** to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_static_files_container_labels_base_domain_enabled: true
```

Doing this, the playbook will:

- obtain an SSL certificate for the base domain, just like it does for all other domains (see [how we handle SSL certificates](configuring-playbook-ssl-certificates.md))

- serve the `/.well-known/matrix/*` files which are necessary for [Federation Server Discovery](configuring-well-known.md#federation-server-discovery) (also see [Server Delegation](howto-server-delegation.md)) and [Client-Server discovery](configuring-well-known.md#client-server-discovery)

- serve a simple homepage at `https://example.com` with content `Hello from example.com` (configurable via the `matrix_static_files_file_index_html_template` variable). You can also [serve a more complicated static website](#serving-a-static-website-at-the-base-domain).

## Serving a static website at the base domain

By default, when "serving the base domain" is enabled, the playbook hosts a simple `index.html` webpage at `/matrix/static-files/public/index.html`. The content of this page is taken from the `matrix_static_files_file_index_html_template` variable.

If you'd like to host your own static website (more than a single `index.html` page) at the base domain, you can disable the creation of this default `index.html` page like this:

```yaml
# Enable base-domain serving
matrix_static_files_container_labels_base_domain_enabled: true

# Prevent the default index.html file from being installed
matrix_static_files_file_index_html_enabled: false

# Disable the automatic redirectin of `https://example.com/` to `https://matrix.example.com/`.
# This gets automatically enabled when you disable `matrix_static_files_file_index_html_enabled`, as we're doing above.
matrix_static_files_container_labels_base_domain_root_path_redirection_enabled: false
```

With this configuration, Ansible will no longer mess around with the `/matrix/static-files/public/index.html` file.

You are then free to upload any static website files to `/matrix/static-files/public` and they will get served at the base domain. You can do so manually or by using the [ansible-role-aux](https://github.com/mother-of-all-self-hosting/ansible-role-aux) Ansible role, which is part of this playbook already.

## Serving a more complicated website at the base domain

If you'd like to serve an even more complicated (dynamic) website from the Matrix server, relying on the playbook to serve the base domain is not the best choice.

You have 2 options.

**One way is to host your base domain elsewhere**. This involves:
- you stopping to serve it from the Matrix server: remove `matrix_static_files_container_labels_base_domain_enabled` from your configuration
- [configuring Matrix Delegation via well-known](./configuring-well-known.md)

**Another way is to serve the base domain from another (your own) container on the Matrix server**. This involves:
- telling the playbook to only serve `example.com/.well-known/matrix` files by adjusting your `vars.yml` configuration like this:
  - keep `matrix_static_files_container_labels_base_domain_enabled: true`
  - add an extra: `matrix_static_files_container_labels_base_domain_traefik_path_prefix: /.well-known/matrix`
- building and running a new container on the Matrix server:
  - it should be connected to the `traefik` network, so that Traefik can reverse-proxy to it
  - it should have appropriate [container labels](https://docs.docker.com/config/labels-custom-metadata/), which instruct Traefik to reverse-proxy to it

How you'll be managing building and running this container is up-to-you. You may use of the primitives from [ansible-role-aux](https://github.com/mother-of-all-self-hosting/ansible-role-aux) Ansible role to organize it yourself, or you can set it up in another way.
