# Server Delegation via a DNS SRV record (advanced)

**Reminder** : unless you are affected by the [Downsides of well-known-based Server Delegation](howto-server-delegation.md#downsides-of-well-known-based-server-delegation), we suggest you **stay on the simple/default path**: [Server Delegation](howto-server-delegation.md) by [configuring well-known files](configuring-well-known.md) at the base domain. 

This guide is about configuring Server Delegation using DNS SRV records (for the [Traefik](https://doc.traefik.io/traefik/) webserver). This method has special requirements when it comes to SSL certificates, so various changes are required.

## Prerequisites

SRV delegation while still using the playbook provided Traefik to get / renew the certificate requires a wildcard certificate.

To obtain / renew one from [Let's Encrypt](https://letsencrypt.org/), one needs to use a [DNS-01 challenge](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) method instead of the default [HTTP-01](https://letsencrypt.org/docs/challenge-types/#http-01-challenge).

This means that this is **limited to the list of DNS providers supported by Traefik**, unless you bring in your own certificate.

The up-to-date list can be accessed on [traefik's documentation](https://doc.traefik.io/traefik/https/acme/#providers)

## The changes

### Federation Endpoint

```yaml
# To serve the federation from any domain, as long as the path match
matrix_nginx_proxy_container_labels_traefik_proxy_matrix_federation_rule: PathPrefix(`/_matrix`)
```

This is because with SRV federation, some servers / tools (one of which being the federation tester) try to access the federation API using the resolved IP address instead of the domain name (or they are not using SNI). This change will make Traefik route all traffic for which the path match this rule go to the federation endpoint.

### Tell Traefik which certificate to serve for the federation endpoint

Now that the federation endpoint is not bound to a domain anymore we need to explicitely tell Traefik to use a wildcard certificate in addition to one containing the base name.

This is because the matrix specification expects the federation endpoint to be served using a certificate comatible with the base domain, however, the other resources on the endpoint still need a valid certificate to work.

```yaml
# To let Traefik know which domains' certificates to serve
matrix_nginx_proxy_container_labels_additional_labels: |
  traefik.http.routers.matrix-nginx-proxy-matrix-federation.tls.domains.main="example.com"
  traefik.http.routers.matrix-nginx-proxy-matrix-federation.tls.domains.sans="*.example.com"
```

### Configure the DNS-01 challenge for let's encrypt

Since we're now requesting a wildcard certificate, we need to change the ACME challenge method. To request a wildcard certificate from Let's Encrypt we are required to use the DNS-01 challenge.

This will need 3 changes:
1. Add a new certificate resolver that works with DNS-01
2. Configure the resolver to allow access to the DNS zone to configure the records to answer the challenge (refer to [Traefik's documentation](https://doc.traefik.io/traefik/https/acme/#providers) to know which environment variables to set)
3. Tell the playbook to use the new resolver as default

We cannot just disable the default resolver as that would disable SSL in quite a few places in the playbook.

```yaml
# 1. Add a new ACME configuration without having to disable the default one, since it would have a wide range of side effects
devture_traefik_configuration_extension_yaml: |
  certificatesResolvers:
    dns:
      acme:
        # To use a staging endpoint for testing purposes, uncomment the line below.
        # caServer: https://acme-staging-v02.api.letsencrypt.org/directory
        email: {{ devture_traefik_config_certificatesResolvers_acme_email | to_json }}
        dnsChallenge:
          provider: cloudflare
          resolvers: 
            - "1.1.1.1:53"
            - "8.8.8.8:53"
        storage: {{ devture_traefik_config_certificatesResolvers_acme_storage | to_json }}

# 2. Configure the environment variables needed by Rraefik to automate the ACME DNS Challenge (example for Cloudflare)
devture_traefik_environment_variables: |
  CF_API_EMAIL=redacted
  CF_ZONE_API_TOKEN=redacted
  CF_DNS_API_TOKEN=redacted
  LEGO_DISABLE_CNAME_SUPPORT=true

# 3. Instruct the playbook to use the new ACME configuration
devture_traefik_certResolver_primary: dns
```

## Adjust Coturn's configuration

The last step is to alter the generated Coturn configuration.

By default, Coturn is configured to wait on the certificate for the `matrix.` subdomain using an [instantiated systemd service](https://www.freedesktop.org/software/systemd/man/systemd.service.html#Service%20Templates) using the domain name as the parameter for this service. However, we need to serve the wildcard certificate, which is incompatible with systemd, it will try to expand the `*`, which will break and prevent Coturn from starting.

We also need to indicate to Coturn where the wildcard certificate is.

**⚠ WARNING ⚠** : On first start of the services, Coturn might still fail to start because Traefik is still in the process of obtaining the certificates. If you still get an error, make sure Traefik obtained the certificates and restart the Coturn service (`just start-group coturn`).

This should not happen again afterwards as Traefik will renew certificates well before their expiry date, and the Coturn service is setup to restart periodically.

```yaml
# Only depend on docker.service, this removes the dependency on the certificate exporter, might imply the need to manually restart coturn on the first installation once the certificates are obtained, afterwards, the reload service should handle things
matrix_coturn_systemd_required_services_list: ['docker.service']

# This changes the path of the loaded certificate, while maintaining the original functionality, we're now loading the wildcard certificate.
matrix_coturn_container_additional_volumes: |
  {{
    (
      [
       {
         'src': (matrix_ssl_config_dir_path + '/live/*.' + matrix_domain + '/fullchain.pem'),
         'dst': '/fullchain.pem',
         'options': 'ro',
       },
       {
         'src': (matrix_ssl_config_dir_path + '/live/*.' + matrix_domain + '/privkey.pem'),
         'dst': '/privkey.pem',
         'options': 'ro',
       },
      ] if matrix_playbook_reverse_proxy_type in ['playbook-managed-nginx', 'other-nginx-non-container'] and matrix_coturn_tls_enabled else []
    )
    +
    (
      [
       {
         'src': (devture_traefik_certs_dumper_dumped_certificates_dir_path +  '/*.' + matrix_domain + '/certificate.crt'),
         'dst': '/certificate.crt',
         'options': 'ro',
       },
       {
         'src': (devture_traefik_certs_dumper_dumped_certificates_dir_path +  '/*.' + matrix_domain + '/privatekey.key'),
         'dst': '/privatekey.key',
         'options': 'ro',
       },
      ] if matrix_playbook_reverse_proxy_type in ['playbook-managed-traefik', 'other-traefik-container'] and devture_traefik_certs_dumper_enabled and matrix_coturn_tls_enabled else []
    )
  }}
```

## Full example of a working configuration

```yaml
# Choosing the reverse proxy implementation
matrix_playbook_reverse_proxy_type: playbook-managed-traefik
devture_traefik_config_certificatesResolvers_acme_email: redacted@example.com

# To serve the federation from any domain, as long as the path match
matrix_nginx_proxy_container_labels_traefik_proxy_matrix_federation_rule: PathPrefix(`/_matrix`)

# To let Traefik know which domains' certificates to serve
matrix_nginx_proxy_container_labels_additional_labels: |
  traefik.http.routers.matrix-nginx-proxy-matrix-federation.tls.domains.main="example.com"
  traefik.http.routers.matrix-nginx-proxy-matrix-federation.tls.domains.sans="*.example.com"

# Add a new ACME configuration without having to disable the default one, since it would have a wide range of side effects
devture_traefik_configuration_extension_yaml: |
  certificatesResolvers:
    dns:
      acme:
        # To use a staging endpoint for testing purposes, uncomment the line below.
        # caServer: https://acme-staging-v02.api.letsencrypt.org/directory
        email: {{ devture_traefik_config_certificatesResolvers_acme_email | to_json }}
        dnsChallenge:
          provider: cloudflare
          resolvers: 
            - "1.1.1.1:53"
            - "8.8.8.8:53"
        storage: {{ devture_traefik_config_certificatesResolvers_acme_storage | to_json }}

# Instruct thep laybook to use the new ACME configuration
devture_traefik_certResolver_primary: "dns"

# Configure the environment variables needed by Traefik to automate the ACME DNS Challenge (example for Cloudflare)
devture_traefik_environment_variables: |
  CF_API_EMAIL=redacted
  CF_ZONE_API_TOKEN=redacted
  CF_DNS_API_TOKEN=redacted
  LEGO_DISABLE_CNAME_SUPPORT=true

# Only depend on docker.service, this removes the dependency on the certificate exporter, might imply the need to manually restart Coturn on the first installation once the certificates are obtained, afterwards, the reload service should handle things
matrix_coturn_systemd_required_services_list: ['docker.service']

# This changes the path of the loaded certificate, while maintaining the original functionality, we're now loading the wildcard certificate.
matrix_coturn_container_additional_volumes: |
  {{
    (
      [
       {
         'src': (matrix_ssl_config_dir_path + '/live/*.' + matrix_domain + '/fullchain.pem'),
         'dst': '/fullchain.pem',
         'options': 'ro',
       },
       {
         'src': (matrix_ssl_config_dir_path + '/live/*.' + matrix_domain + '/privkey.pem'),
         'dst': '/privkey.pem',
         'options': 'ro',
       },
      ] if matrix_playbook_reverse_proxy_type in ['playbook-managed-nginx', 'other-nginx-non-container'] and matrix_coturn_tls_enabled else []
    )
    +
    (
      [
       {
         'src': (devture_traefik_certs_dumper_dumped_certificates_dir_path +  '/*.' + matrix_domain + '/certificate.crt'),
         'dst': '/certificate.crt',
         'options': 'ro',
       },
       {
         'src': (devture_traefik_certs_dumper_dumped_certificates_dir_path +  '/*.' + matrix_domain + '/privatekey.key'),
         'dst': '/privatekey.key',
         'options': 'ro',
       },
      ] if matrix_playbook_reverse_proxy_type in ['playbook-managed-traefik', 'other-traefik-container'] and devture_traefik_certs_dumper_enabled and matrix_coturn_tls_enabled else []
    )
  }}
```
