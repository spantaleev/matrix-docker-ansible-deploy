# Adjusting SSL certificate retrieval (optional, advanced)

By default, this playbook retrieves and auto-renews free SSL certificates from [Let's Encrypt](https://letsencrypt.org/) for the domains it needs (`matrix.<your-domain>` and possibly others).

Those certificates are used when configuring the nginx reverse proxy installed by this playbook.
They can also be used for configuring [your own webserver](configuring-playbook-own-webserver.md), in case you're not using the integrated nginx server provided by the playbook.

If you need to retrieve certificates for other domains (e.g. your base domain) or more control over certificate retrieval, read below.

Things discussed in this document:

- [Using self-signed SSL certificates](#using-self-signed-ssl-certificates), if you can't use Let's Encrypt or just need a test setup

- [Using your own SSL certificates](#using-your-own-ssl-certificates), if you don't want to or can't use Let's Encrypt certificates, but are still interested in using the integrated nginx reverse proxy server

- [Not bothering with SSL certificates](#not-bothering-with-ssl-certificates), if you're using [your own webserver](configuring-playbook-own-webserver.md) and would rather this playbook leaves SSL certificate management to you

- [Obtaining SSL certificates for additional domains](#obtaining-ssl-certificates-for-additional-domains), if you'd like to host additional domains on the Matrix server and would like the playbook to help you obtain and renew certificates for those domains automatically

- [Using DNS challenge to obtain Let's encrypt SSL certificates](#using-dns-challenge-to-obtain-lets-encrypt-ssl-certificates), if you'd like to host additional domains on the Matrix server and would like the playbook to help you obtain and renew certificates for those domains automatically

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
- `<matrix_ssl_config_dir_path>/live/<domain>/chain.pem`

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
- possibly for `hydrogen.<your-domain>`, if you have explicitly [set up Hydrogen client](configuring-playbook-client-hydrogen.md).
- possibly for `cinny.<your-domain>`, if you have explicitly [set up Cinny client](configuring-playbook-client-cinny.md).
- possibly for `dimension.<your-domain>`, if you have explicitly [set up Dimension](configuring-playbook-dimension.md).
- possibly for `goneb.<your-domain>`, if you have explicitly [set up Go-NEB bot](configuring-playbook-bot-go-neb.md).
- possibly for `jitsi.<your-domain>`, if you have explicitly [set up Jitsi](configuring-playbook-jitsi.md).
- possibly for `stats.<your-domain>`, if you have explicitly [set up Grafana](configuring-playbook-prometheus-grafana.md).
- possibly for `sygnal.<your-domain>`, if you have explicitly [set up Sygnal](configuring-playbook-sygnal.md).
- possibly for `ntfy.<your-domain>`, if you have explicitly [set up ntfy](configuring-playbook-ntfy.md).
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

## Specify the SSL private key algorithm

If you'd like to [specify the private key type](https://eff-certbot.readthedocs.io/en/stable/using.html#using-ecdsa-keys) used with Let's Encrypt, define your own custom configuration like this:

```yaml
matrix_ssl_lets_encrypt_key_type: ecdsa
```

## Using DNS challenge to obtain Let's encrypt SSL certificates

Let's encrypt proposes different challenges prior delivering a certificate (https://letsencrypt.org/docs/challenge-types/).

By default, this playbook uses HTTP challenges to request for Let's encrypt certificates.

For some domains and in specific cases (e.g. no HTTP server on the matrix base domain), relying on a DNS challenge is the only possible solution.

First of all, the domain to retrieve the certificate for must be in the list of domains to retrieve certificates for: `matrix_ssl_domains_to_obtain_certificates_for`.
Please see [Obtaining SSL certificates for additional domains](#obtaining-ssl-certificates-for-additional-domains) for more details about how to configure this list.

### Configure the cerbot image to use

In order to retrieve a certificate through DNS challenge, Cerbot must use a plugin adapted to the DNS provider which will answer to the challenge.

By default, the playbook uses the main Cerbot image which has no plugins configured.

To use an official Cerbot image with a plugin for DNS challenge, you must set `matrix_ssl_lets_encrypt_certbot_challenge_image` to 'dns' (default is 'http') and indicate the DNS plugin to use with `matrix_ssl_lets_encrypt_certbot_official_dns_provider`.

```yaml
# In this example, we use the cerbot official with its plugin for doing DNS challenges using OVH.
matrix_ssl_lets_encrypt_certbot_challenge_image: 'dns'
matrix_ssl_lets_encrypt_certbot_official_dns_provider: 'ovh'
```

Supported DNS providers/methods are (https://eff-certbot.readthedocs.io/en/stable/using.html#dns-plugins):
- Cloudflare: `cloudflare`
- CloudXNS: `cloudxns`
- DigitalOcean: `digitalocean`
- DNS Made Easy: `dnsmadeeasy`
- DNSimple: `dnsimple`
- Gehirn: `gehirn`
- Google Cloud DNS: `google`
- Linode: `linode`
- LuaDNS: `luadns`
- NS1: `nsone`
- OVH: `ovh`
- RFC 2136 Dynamic Updates: `rfc2136`
- Amazon Route 53: `route53`
- Sakura Cloud: `sakuracloud`

Some advanced users may need to use a custom certbot image to configure multiple DNS plugins.
To do so, you can set `matrix_ssl_lets_encrypt_certbot_challenge_image` to 'custom' and indicate which image to use with `matrix_ssl_lets_encrypt_certbot_custom_docker_image`.
This image must have similar behavior as cerbot official images for DNS plugins.

```yaml
# For advanced users only
matrix_ssl_lets_encrypt_certbot_challenge_image: 'custom'
matrix_ssl_lets_encrypt_certbot_custom_docker_image: "{{ matrix_container_global_registry_prefix }}my-custom/image:v1.0.0"
```

### Prepare the configuration file for plugin authentication

DNS plugins rely on configuration files which must be declared in an entry of `matrix_ssl_lets_encrypt_dns_config`.
Each entry must contain:
- a `name` which will be referenced by the domain (so that same configuration can be used for multiple domains)
- a `template` among those supported in the roles/matrix-nginx-proxy/templates/dns-config folder (without the .j2 extension)
- a list of the properties required by the plugin for authentication 

The properties to use are the named arguments listed in the cerbot plugin documentation, removing the leading double dashes ('--') and replacing other dashes ('-') by underscore ('_'):
- Cloudflare: https://certbot-dns-cloudflare.readthedocs.io/en/stable/#
- CloudXNS: https://certbot-dns-cloudxns.readthedocs.io/en/stable/#
- DigitalOcean: https://certbot-dns-digitalocean.readthedocs.io/en/stable/#
- DNS Made Easy: https://certbot-dns-dnsmadeeasy.readthedocs.io/en/stable/#
- DNSimple: https://certbot-dns-dnsimple.readthedocs.io/en/stable/#
- Gehirn: https://certbot-dns-gehirn.readthedocs.io/en/stable/#
- Google Cloud DNS: https://certbot-dns-google.readthedocs.io/en/stable/#
- Linode: https://certbot-dns-linode.readthedocs.io/en/stable/#
- LuaDNS: https://certbot-dns-luadns.readthedocs.io/en/stable/#
- NS1: https://certbot-dns-nsone.readthedocs.io/en/stable/#
- OVH: https://certbot-dns-ovh.readthedocs.io/en/stable/#
- RFC 2136 Dynamic Updates: https://certbot-dns-rfc2136.readthedocs.io/en/stable/#
- Amazon Route 53: https://certbot-dns-route53.readthedocs.io/en/stable/#
- Sakura Cloud: https://certbot-dns-sakuracloud.readthedocs.io/en/stable/#

```yaml
# In this example, we use OVH official DNS cerbot plugin to create a 'myovh.ini' configuration file.
matrix_ssl_lets_encrypt_dns_config:
  - name: 'myovh.ini'
    template: 'ovh.ini'
    dns_ovh_endpoint: 'ovh-eu'
    dns_ovh_application_key: '{{ vault_ovh_application_key }}'
    dns_ovh_application_secret: '{{ vault_ovh_application_secret }}'
    dns_ovh_consumer_key: '{{ vault_ovh_consumer_key }}'
```

Beware that all generated configuration files will be mapped within all docker containers used for let's encrypt, whether they are needed or not!!!

For using Route53 DNS plugin, a pre-hook script is used with cerbot in order to link ~/.aws/config to the relevant configuration file.

### Declare which domain to use DNS challenge for

Last but not least, the domain has to be configured with the provider to use in cerbot command and the name of a previously created configuration.

Supported providers are:
- Cloudflare: `cloudflare`
- CloudXNS: `cloudxns`
- DigitalOcean: `digitalocean`
- DNS Made Easy: `dnsmadeeasy`
- DNSimple: `dnsimple`
- Gehirn: `gehirn`
- Google Cloud DNS: `google`
- Linode: `linode`
- LuaDNS: `luadns`
- NS1: `nsone`
- OVH: `ovh`
- RFC 2136 Dynamic Updates: `rfc2136`
- Amazon Route 53: `route53`
- Sakura Cloud: `sakuracloud`

```yaml
# In this example, we use cerbot OVH command with the previously created 'myovh.ini' configuration.
matrix_ssl_lets_encrypt_dns_challenge_domains:
  - domain: '{{ matrix_domain }}'
    provider: 'ovh'
    config_file: 'myovh.ini'
```

### Example configuration for base domain and OVH provider

Complete example configuration to get certificate for the matrix domain with a DNS challenge to OVH DNS provider.

```yaml
# In this example, we retrieve an extra certificate for
# the matrix base domain through DNS challenge to OVH DNS provider
# and we use it for the federation API.
# All other domains but the matrix base domain will use HTTP challenge.

# Retrieve an extra certificate for
# the base domain (in the `matrix_domain` variable).
matrix_ssl_additional_domains_to_obtain_certificates_for:
  - '{{ matrix_domain }}'

# Use an image with the plugin for doing DNS challenges using OVH instead of the default one
# Other official images are supported by adapting the `matrix_ssl_lets_encrypt_certbot_official_dns_provider` variable.
matrix_ssl_lets_encrypt_certbot_challenge_image: 'dns'
matrix_ssl_lets_encrypt_certbot_official_dns_provider: 'ovh'

# Provide configuration for DNS plugin
# Other configuration for official plugins are supported by adapting the `template` variable of a configuration.
matrix_ssl_lets_encrypt_dns_config:
  - name: 'ovh.ini'
    template: 'ovh.ini'
    dns_ovh_endpoint: 'ovh-eu'
    dns_ovh_application_key: '{{ vault_ovh_application_key }}'
    dns_ovh_application_secret: '{{ vault_ovh_application_secret }}'
    dns_ovh_consumer_key: '{{ vault_ovh_consumer_key }}'

# Configure retrieval of certificate for the base domain
# through DNS challenge with previously created configuration.
matrix_ssl_lets_encrypt_dns_challenge_domains:
  - domain: '{{ matrix_domain }}'
    provider: 'ovh'
    config_file: 'ovh.ini'

# Configure the base domain certificate to be used
# by Federation API instead of the matrix domain one `matrix.{{ matrix_domain }}`.
matrix_nginx_proxy_proxy_matrix_federation_api_ssl_certificate: '/matrix/ssl/config/live/{{ matrix_domain }}/fullchain.pem'
matrix_nginx_proxy_proxy_matrix_federation_api_ssl_certificate_key: '/matrix/ssl/config/live/{{ matrix_domain }}/privkey.pem'

```
