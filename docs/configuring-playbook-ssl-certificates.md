# Adjusting SSL certificate retrieval (optional, advanced)

By default, this playbook retrieves and auto-renews free SSL certificates from [Let's Encrypt](https://letsencrypt.org/) for the domains it needs (`matrix.<your-domain>` and possibly `element.<your-domain>`)

Those certificates are used when configuring the nginx reverse proxy installed by this playbook.
They can also be used for configuring [your own webserver](configuring-playbook-own-webserver.md), in case you're not using the integrated nginx server provided by the playbook.

If you need to retrieve certificates for other domains (e.g. your base domain) or more control over certificate retrieval, read below.

Things discussed in this document:

- [Using self-signed SSL certificates](#using-self-signed-ssl-certificates), if you can't use Let's Encrypt or just need a test setup

- [Using your own SSL certificates](#using-your-own-ssl-certificates), if you don't want to or can't use Let's Encrypt certificates, but are still interested in using the integrated nginx reverse proxy server

- [Not bothering with SSL certificates](#not-bothering-with-ssl-certificates), if you're using [your own webserver](configuring-playbook-own-webserver.md) and would rather this playbook leaves SSL certificate management to you

- [Obtaining SSL certificates for additional domains](#obtaining-ssl-certificates-for-additional-domains), if you'd like to host additional domains on the Matrix server and would like the playbook to help you obtain and renew certificates for those domains automatically


## Using self-signed SSL certificates

For private deployments (not publicly accessible from the internet), you may not be able to use Let's Encrypt certificates.

If self-signed certificates are alright with you, you can ask the playbook to generate such for you with the following configuration:

```yaml
matrix_ssl_retrieval_method: self-signed
```

If you get a `Cannot reach homeserver` error in Element, you will have to visit `https://matrix.<your-domain>` in your browser and agree to the certificate exception before you can login.


## Using your own SSL certificates

If you'd like to manage SSL certificates by yourself and have the playbook use your certificate files, you can use the following configuration:

```yaml
matrix_ssl_retrieval_method: manually-managed
```

With such a configuration, the playbook would expect you to drop the SSL certificate files in the directory specified by `matrix_ssl_config_dir_path` (`/matrix/ssl/config` by default) obeying the following hierarchy:

- `<matrix_ssl_config_dir_path>/live/<domain>/fullchain.pem`
- `<matrix_ssl_config_dir_path>/live/<domain>/privkey.pem`

where `<domain>` refers to the domains that you need (usually `matrix.<your-domain>` and `element.<your-domain>`).


## Not bothering with SSL certificates

If you're [using an external web server](configuring-playbook-own-webserver.md) which is not nginx, or you would otherwise want to manage its certificates without this playbook getting in the way, you can completely disable SSL certificate management with the following configuration:

```yaml
matrix_ssl_retrieval_method: none
```

With such a configuration, no certificates will be retrieved at all. You're free to manage them however you want.


## Obtaining SSL certificates for additional domains

The playbook tries to be smart about the certificates it will obtain for you.

By default, it obtains certificates for:
- `matrix.<your-domain>` (`matrix_server_fqn_matrix`)
- possibly for `element.<your-domain>`, unless you have disabled the [Element client component](configuring-playbook-client-element.md) using `matrix_client_element_enabled: false`
- possibly for `riot.<your-domain>`, if you have explicitly enabled Riot to Element redirection (for background compatibility) using `matrix_nginx_proxy_proxy_riot_compat_redirect_enabled: true`
- possibly for `dimension.<your-domain>`, if you have explicitly [set up Dimension](configuring-playbook-dimension.md).
- possibly for `jitsi.<your-domain>`, if you have explicitly [set up Jitsi](configuring-playbook-jitsi.md).
- possibly for your base domain (`<your-domain>`), if you have explicitly configured [Serving the base domain](configuring-playbook-base-domain-serving.md)

If you are hosting other domains on the Matrix machine, you can make the playbook obtain and renew certificates for those other domains too.
To do that, simply define your own custom configuration like this:

```yaml
# In this example, we retrieve 2 extra certificates,
# one for the base domain (in the `matrix_domain` variable) and one for a hardcoded domain.
# Adding any other additional domains (hosted on the same machine) is possible.
matrix_ssl_additional_domains_to_obtain_certificates_for:
  - '{{ matrix_domain }}'
  - 'another.domain.example.com'
```

After redefining `matrix_ssl_domains_to_obtain_certificates_for`, to actually obtain certificates you should:

- make sure the web server occupying port 80 is stopped. If you are using matrix-nginx-proxy server (which is the default for this playbook), you need to stop it temporarily by running `systemctl stop matrix-nginx-proxy` on the server.

- re-run the SSL part of the playbook and restart all services: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-ssl,start`

The certificate files would be made available in `/matrix/ssl/config/live/<your-other-domain>/...`.

For automated certificate renewal to work, each port `80` vhost for each domain you are obtaining certificates for needs to forward requests for `/.well-known/acme-challenge` to the certbot container we use for renewal.

See how this is configured for the `matrix.` subdomain in `/matrix/nginx-proxy/conf.d/matrix-synapse.conf`
Don't be alarmed if the above configuration file says port `8080`, instead of port `80`. It's due to port mapping due to our use of containers.
