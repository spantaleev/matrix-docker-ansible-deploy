# Adjusting SSL certificate retrieval (optional, advanced)

By default, this playbook retrieves and auto-renews free SSL certificates from [Let's Encrypt](https://letsencrypt.org/) for the domains it needs (e.g. `matrix.<your-domain>` and others)

This guide is about using the integrated Traefik server and doesn't apply if you're using [your own webserver](configuring-playbook-own-webserver.md).


## Using staging Let's Encrypt certificates instead of real ones

For testing purposes, you may wish to use staging certificates provide by Let's Encrypt.

You can do this with the following configuration:

```yaml
devture_traefik_config_certificatesResolvers_acme_use_staging: true
```


## Disabling SSL termination

For testing or other purposes, you may wish to install services without SSL termination and have services exposed to `http://` instead of `https://`.

You can do this with the following configuration:

```yaml
devture_traefik_config_entrypoint_web_secure_enabled: false
```


## Using self-signed SSL certificates

If you'd like to use your own SSL certificates, instead of the default (SSL certificates obtained automatically via [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) from [Let's Encrypt](https://letsencrypt.org/)):

- generate your self-signed certificate files
- follow the [Using your own SSL certificates](#using-your-own-ssl-certificates) documentation below


## Using your own SSL certificates

To use your own SSL certificates with Traefik, you need to:

- disable [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) / [Let's Encrypt](https://letsencrypt.org/) support
- put a custom Traefik configuration file on the server, with the help of this Ansible playbook (via the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux)) or manually
- register your custom configuration file with Traefik, by adding an extra provider of type [file](https://doc.traefik.io/traefik/providers/file/)
- put the SSL files on the server, with the help of this Ansible playbook (via the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux)) or manually

```yaml
# Disable ACME / Let's Encrypt support.
devture_traefik_config_certificatesResolvers_acme_enabled: false

# Disabling ACME support (above) automatically disables the creation of the SSL directory.
# Force-enable it here, because we'll add our certificate files there.
devture_traefik_ssl_dir_enabled: true

# Tell Traefik to load our custom configuration file (certificates.yml).
# The file is created below, in `aux_file_definitions`.
# The `/config/..` path is an in-container path, not a path on the host (like `/matrix/traefik/config`). Do not change it!
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      filename: /config/certificates.yml
      watch: true

# Use the aux role to create our custom files on the server.
# If you'd like to do this manually, you remove this `aux_file_definitions` variable.
aux_file_definitions:
  # Create the privkey.pem file on the server by
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ devture_traefik_ssl_dir_path }}/privkey.pem"
    src: /path/on/your/Ansible/computer/to/privkey.pem
    # Alternatively, comment out `src` above and uncomment the lines below to provide the certificate content inline.
    # Note the indentation level.
    # content: |
    #   FILE CONTENT
    #   HERE

  # Create the cert.pem file on the server
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ devture_traefik_ssl_dir_path }}/cert.pem"
    src: /path/on/your/Ansible/computer/to/cert.pem
    # Alternatively, comment out `src` above and uncomment the lines below to provide the certificate content inline.
    # Note the indentation level.
    # content: |
    #   FILE CONTENT
    #   HERE

  # Create the custom Traefik configuration.
  # The `/ssl/..` paths below are in-container paths, not paths on the host (/`matrix/traefik/ssl/..`). Do not change them!
  - dest: "{{ devture_traefik_config_dir_path }}/certificates.yml"
    content: |
      tls:
        certificates:
          - certFile: /ssl/cert.pem
            keyFile: /ssl/privkey.pem
        stores:
          default:
            defaultCertificate:
              certFile: /ssl/cert.pem
              keyFile: /ssl/privkey.pem
```

## Using a DNS-01 ACME challenge type, instead of HTTP-01

You can configure Traefik to use the [DNS-01 challenge type](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) for Let's Encrypt. This is less commonly used than the default [HTTP-01 challenge type](https://letsencrypt.org/docs/challenge-types/#http-01-challenge), but it can be helpful to:

- hide your public IP from Let's Encrypt logs
- allow you to obtain SSL certificates for servers which are not accessible (via HTTP) from the public internet (and for which the HTTP-01 challenge would fail)

This is an example for how to edit the `vars.yml` file if you're using Cloudflare:

```yaml
devture_traefik_config_certificatesResolvers_acme_dnsChallenge_enabled: true
devture_traefik_config_certificatesResolvers_acme_dnsChallenge_provider: "cloudflare"
devture_traefik_config_certificatesResolvers_acme_dnsChallenge_delayBeforeCheck: 60
devture_traefik_config_certificatesResolvers_acme_dnsChallenge_resolvers:
  - "1.1.1.1:53"
devture_traefik_environment_variables_additional_variables: |
  CF_API_EMAIL=redacted
  CF_ZONE_API_TOKEN=redacted
  CF_DNS_API_TOKEN=redacted
  LEGO_DISABLE_CNAME_SUPPORT=true
```

Make sure to change the value of "provider" to your particular DNS solution, and provide the appropriate environment variables. The full list of supported providers is available [here](https://doc.traefik.io/traefik/https/acme/#providers).

This example assumes you're using Cloudflare to manage your DNS zone. Note that it requires the use of two tokens: one for reading all zones (`CF_ZONE_API_TOKEN`) and another that must be able to edit the particular domain you're using (`CF_DNS_API_TOKEN`). For security, it's recommended that you create two fine-grained tokens for this purpose, but you might choose to use the same token for both.
