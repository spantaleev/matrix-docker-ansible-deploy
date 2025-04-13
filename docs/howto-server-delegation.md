<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2019 Julian Foad
SPDX-FileCopyrightText: 2020 Ivar Troost
SPDX-FileCopyrightText: 2020 Julian Strobl
SPDX-FileCopyrightText: 2021 MDAD project contributors
SPDX-FileCopyrightText: 2023 Antoine-Ali Zarrouk
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Server Delegation

By default, this playbook sets up services on your Matrix server (`matrix.example.com`). To have this server officially be responsible for Matrix services for the base domain (`example.com`), you need to set up server delegation / redirection.

Server delegation can be configured in either of these ways:

- [Setting up a `/.well-known/matrix/server` file](#server-delegation-via-a-well-known-file) on the base domain (`example.com`)
- [Setting up a `_matrix._tcp` DNS SRV record](#server-delegation-via-a-dns-srv-record-advanced)

Both methods have their place and will continue to do so. You only need to use just one of these delegation methods.

For simplicity reasons, this playbook recommends you to set up server delegation via a `/.well-known/matrix/server` file. However, that method may have some downsides that are not to your liking. Hence this guide about alternative ways to set up Server Delegation.

**Note**: as an alternative, it is possible to install the server such that it uses only the `matrix.example.com` domain (instead of identifying as the shorter base domain — `example.com`). This should be helpful if you are not in control of anything on the base domain (`example.com`). In this case, you would not need to configure server delegation, but you would need to add other configuration. For more information, see [How do I install on matrix.example.com without involving the base domain?](faq.md#how-do-i-install-on-matrix-example-com-without-involving-the-base-domain) on our FAQ.

## Server Delegation via a well-known file

This playbook recommends you to set up server delegation by means of a `/.well-known/matrix/server` file served from the base domain (`example.com`), as this is the most straightforward way to set up the delegation.

To configure server delegation with the well-known file, check this section on [Configuring Service Discovery via .well-known](configuring-well-known.md): [Installing well-known files on the base domain's server](configuring-well-known.md#installing-well-known-files-on-the-base-domain-s-server)

### Downsides of well-known-based Server Delegation

Server Delegation by means of a `/.well-known/matrix/server` file is the most straightforward, but suffers from the following downsides:

- you need to have a working HTTPS server for the base domain (`example.com`). If you don't have any server for the base domain at all, you can easily solve it by making the playbook [serve the base domain from the Matrix server](configuring-playbook-base-domain-serving.md).

- any downtime on the base domain (`example.com`) or network trouble between the Matrix subdomain (`matrix.example.com`) and the base `example.com` may cause Matrix Federation outages. As the [Server-Server spec says](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery):

> Errors are recommended to be cached for up to an hour, and servers are encouraged to exponentially back off for repeated failures.

**For most people, this is a reasonable tradeoff** given that it's easy and straightforward to set up. We recommend you stay on this path.

Otherwise, you can decide to go against the default for this playbook, and instead set up [Server Delegation via a DNS SRV record (advanced)](#server-delegation-via-a-dns-srv-record-advanced) (much more complicated).

## Server Delegation via a DNS SRV record (advanced)

**Note**: doing Server Delegation via a DNS SRV record is a more **advanced** way to do it and is not the default for this playbook. This is usually **much more complicated** to set up, so **we don't recommend it**. If you're not an experienced sysadmin, you'd better stay away from this.

As per the [Server-Server spec](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery), it's possible to do Server Delegation using only a SRV record (without a `/.well-known/matrix/server` file).

This prevents you from suffering the [Downsides of well-known-based Server Delegation](#downsides-of-well-known-based-server-delegation).

To use DNS SRV record validation, you need to:

- ensure that `/.well-known/matrix/server` is **not served** from the base domain, as that would interfere with DNS SRV record Server Delegation. To make the playbook **not** generate and serve the file, use the following configuration: `matrix_static_files_file_matrix_server_enabled: false`.

- ensure that you have a `_matrix._tcp` DNS SRV record for your base domain (`example.com`) with a value of `10 0 8448 matrix.example.com`

- ensure that you are serving the Matrix Federation API (tcp/8448) with a certificate for `example.com` (not `matrix.example.com`!). Getting this certificate to the `matrix.example.com` server may be complicated. The playbook's automatic SSL obtaining/renewal flow will likely not work and you'll need to copy certificates around manually. See below.

For more details on how to configure the playbook to work with SRV delegation, take a look at this documentation: [Server Delegation via a DNS SRV record (advanced)](howto-srv-server-delegation.md)

### Obtain certificates

How you can obtain a valid certificate for `example.com` on the `matrix.example.com` server is up to you.

If `example.com` and `matrix.example.com` are hosted on the same machine, you can let the playbook obtain the certificate for you, by following our [Obtaining SSL certificates for additional domains](configuring-playbook-ssl-certificates.md#obtaining-ssl-certificates-for-additional-domains) guide.

If `example.com` and `matrix.example.com` are not hosted on the same machine, you can copy over the certificate files manually. Don't forget that they may get renewed once in a while, so you may also have to transfer them periodically. How often you do that is up to you, as long as the certificate files don't expire.

### Serving the Federation API with your certificates

Regardless of which method for obtaining certificates you've used, once you've managed to get certificates for your base domain onto the `matrix.example.com` machine you can put them to use.

Based on your setup, you have different ways to go about it:

#### Serving the Federation API with your certificates and Synapse handling Federation

You can let Synapse handle Federation by itself.

To do that, make sure the certificate files are mounted into the Synapse container:

```yaml
matrix_synapse_container_extra_arguments:
  - "--mount type=bind,src=/some/path/on/the/host,dst=/some/path/inside/the/container,ro"
```

You can then tell Synapse to serve Federation traffic over TLS on `tcp/8448`:

```yaml
matrix_synapse_tls_federation_listener_enabled: true
matrix_synapse_tls_certificate_path: /some/path/inside/the/container/certificate.crt
matrix_synapse_tls_private_key_path: /some/path/inside/the/container/private.key
```

Make sure to reload Synapse once in a while (`systemctl reload matrix-synapse`), so that newer certificates can kick in. Reloading doesn't cause any downtime.

#### Serving the Federation API with your certificates and another webserver

**Alternatively**, if you are using another webserver, you can set up reverse-proxying for the `tcp/8448` port by yourself. Make sure to use the proper certificates for `example.com` (not for `matrix.example.com`) when serving the `tcp/8448` port.

As recommended in our [Fronting the integrated reverse-proxy webserver with another reverse-proxy](./configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) documentation section, we recommend you to expose the Matrix Federation entrypoint from traffic at a local port (e.g. `127.0.0.1:8449`), so your reverese-proxy should send traffic there.
