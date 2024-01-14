# Server Delegation

To have a server on a subdomain (e.g. `matrix.<your-domain>`) handle Matrix federation traffic for the base domain (`<your-domain>`), we need to instruct the Matrix network of such a delegation.

By default, this playbook guides you into setting up [Server Delegation via a well-known file](#server-delegation-via-a-well-known-file).
However, that method may have some downsides that are not to your liking. Hence this guide about alternative ways to set up Server Delegation.

It is a complicated matter, so unless you are affected by the [Downsides of well-known-based Server Delegation](#downsides-of-well-known-based-server-delegation), we suggest you stay on the simple/default path.


## Server Delegation via a well-known file

Serving a `/.well-known/matrix/server` file from the base domain is the most straightforward way to set up server delegation, but it suffers from some problems that we list in [Downsides of well-known-based Server Delegation](#downsides-of-well-known-based-server-delegation).

As we already mention in [Configuring DNS](configuring-dns.md) and [Configuring Service Discovery via .well-known](configuring-well-known.md),
this playbook already properly guides you into setting up such delegation by means of a `/.well-known/matrix/server` file served from the base domain (`<your-domain>`).

If this is okay with you, feel free to not read ahead.


### Downsides of well-known-based Server Delegation

Server Delegation by means of a `/.well-known/matrix/server` file is the most straightforward, but suffers from the following downsides:

- you need to have a working HTTPS server for the base domain (`<your-domain>`). If you don't have any server for the base domain at all, you can easily solve it by making the playbook [serve the base domain from the Matrix server](configuring-playbook-base-domain-serving.md).

- any downtime on the base domain (`<your-domain>`) or network trouble between the matrix subdomain (`matrix.<your-domain>`) and the base `<domain>` may cause Matrix Federation outages. As the [Server-Server spec says](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery):

> Errors are recommended to be cached for up to an hour, and servers are encouraged to exponentially back off for repeated failures.

**For most people, this is a reasonable tradeoff** given that it's easy and straightforward to set up. We recommend you stay on this path.

Otherwise, you can decide to go against the default for this playbook, and instead set up [Server Delegation via a DNS SRV record (advanced)](#server-delegation-via-a-dns-srv-record-advanced) (much more complicated).


## Server Delegation via a DNS SRV record (advanced)

**NOTE**: doing Server Delegation via a DNS SRV record is a more **advanced** way to do it and is not the default for this playbook. This is usually **much more complicated** to set up, so **we don't recommend it**. If you're not an experience sysadmin, you'd better stay away from this.

As per the [Server-Server spec](https://matrix.org/docs/spec/server_server/r0.1.0.html#server-discovery), it's possible to do Server Delegation using only a SRV record (without a `/.well-known/matrix/server` file).

This prevents you from suffering the [Downsides of well-known-based Server Delegation](#downsides-of-well-known-based-server-delegation).

To use DNS SRV record validation, you need to:

- ensure that `/.well-known/matrix/server` is **not served** from the base domain, as that would interfere with DNS SRV record Server Delegation. To make the playbook **not** generate and serve the file, use the following configuration: `matrix_static_files_file_matrix_server_enabled: false`.

- ensure that you have a `_matrix._tcp` DNS SRV record for your base domain (`<your-domain>`) with a value of `10 0 8448 matrix.<your-domain>`

- ensure that you are serving the Matrix Federation API (tcp/8448) with a certificate for `<your-domain>` (not `matrix.<your-domain>`!). Getting this certificate to the `matrix.<your-domain>` server may be complicated. The playbook's automatic SSL obtaining/renewal flow will likely not work and you'll need to copy certificates around manually. See below.

For more details on [how to configure the playbook to work with SRV delegation](howto-srv-server-delegation.md)

### Obtaining certificates

How you can obtain a valid certificate for `<your-domain>` on the `matrix.<your-domain>` server is up to you.

If `<your-domain>` and `matrix.<your-domain>` are hosted on the same machine, you can let the playbook obtain the certificate for you, by following our [Obtaining SSL certificates for additional domains](configuring-playbook-ssl-certificates.md#obtaining-ssl-certificates-for-additional-domains) guide.

If `<your-domain>` and `matrix.<your-domain>` are not hosted on the same machine, you can copy over the certificate files manually.
Don't forget that they may get renewed once in a while, so you may also have to transfer them periodically. How often you do that is up to you, as long as the certificate files don't expire.


### Serving the Federation API with your certificates

Regardless of which method for obtaining certificates you've used, once you've managed to get certificates for your base domain onto the `matrix.<your-domain>` machine you can put them to use.

Based on your setup, you have different ways to go about it:

- [Server Delegation](#server-delegation)
	- [Server Delegation via a well-known file](#server-delegation-via-a-well-known-file)
		- [Downsides of well-known-based Server Delegation](#downsides-of-well-known-based-server-delegation)
	- [Server Delegation via a DNS SRV record (advanced)](#server-delegation-via-a-dns-srv-record-advanced)
		- [Obtaining certificates](#obtaining-certificates)
		- [Serving the Federation API with your certificates](#serving-the-federation-api-with-your-certificates)
		- [Serving the Federation API with your certificates and another webserver](#serving-the-federation-api-with-your-certificates-and-another-webserver)
		- [Serving the Federation API with your certificates and Synapse handling Federation](#serving-the-federation-api-with-your-certificates-and-synapse-handling-federation)




### Serving the Federation API with your certificates and another webserver

**If you are using some other webserver**, you can set up reverse-proxying for the `tcp/8448` port by yourself.
Make sure to use the proper certificates for `<your-domain>` (not for `matrix.<your-domain>`) when serving the `tcp/8448` port.

As recommended in our [Fronting the integrated reverse-proxy webserver with another reverse-proxy](./configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) documentation section, we recommend you to expose the Matrix Federation entrypoint from traffic at a local port (e.g. `127.0.0.1:8449`), so your reverese-proxy should send traffic there.

### Serving the Federation API with your certificates and Synapse handling Federation

**Alternatively**, you can let Synapse handle Federation by itself.

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

Make sure to reload Synapse once in a while (`systemctl reload matrix-synapse`), so that newer certificates can kick in.
Reloading doesn't cause any downtime.
