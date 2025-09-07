<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2022 Alejo Diaz
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Adjusting SSL certificate retrieval (optional, advanced)

By default, the playbook retrieves and automatically renews free SSL certificates from [Let's Encrypt](https://letsencrypt.org/) via [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) for the domains of the services it installs (e.g. `matrix.example.com` and others). Refer this guide if you want to modify settings about how it manages SSL certificates or have the Traefik server use yours.

**Notes**:
- This guide is intended to be referred for configuring the integrated Traefik server with regard to SSL certificates retrieval. If you're using [your own webserver](configuring-playbook-own-webserver.md), consult its documentation about how to configure it.
- Let's Encrypt ends the expiration notification email service on June 4, 2025 (see: [the official announcement](https://letsencrypt.org/2025/01/22/ending-expiration-emails/)), and it recommends using a third party service for those who want to receive expiration notifications. If you are looking for a self-hosting service, you may be interested in a monitoring tool such as [Update Kuma](https://github.com/louislam/uptime-kuma/).

  The [Mother-of-All-Self-Hosting (MASH)](https://github.com/mother-of-all-self-hosting/mash-playbook) Ansible playbook can be used to install and manage an Uptime Kuma instance. See [this page](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/services/uptime-kuma.md) for the instruction to install it with the MASH playbook. If you are wondering how to use the MASH playbook for your Matrix server, refer [this page](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/setting-up-services-on-mdad-server.md).

## Use staging Let's Encrypt certificates

For testing purposes, you may wish to use staging certificates provided by Let's Encrypt to avoid hitting [its rate limits](https://letsencrypt.org/docs/rate-limits/).

To use ones, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
traefik_config_certificatesResolvers_acme_use_staging: true
```

## Disable SSL termination

For testing or other purposes, you may wish to install services without SSL termination and have services exposed to `http://` instead of `https://`.

To do so, add the following configuration to your `vars.yml` file:

```yaml
traefik_config_entrypoint_web_secure_enabled: false
```

## Use self-signed SSL certificates

To use self-signed certificates, generate them and follow the documentation below about using your own certificates.

## Use your own SSL certificates

To use your own certificates, prepare them and follow the steps below:

- Disable [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) / [Let's Encrypt](https://letsencrypt.org/) support
- Put a custom Traefik configuration file on the server, with the help of this Ansible playbook (via the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux)) or manually
- Register your custom configuration file with Traefik, by adding an extra provider of type [file](https://doc.traefik.io/traefik/providers/file/)
- Put the SSL files on the server, with the help of this Ansible playbook (via the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux)) or manually

For those steps, you can add the following configuration to your `vars.yml` file (adapt to your needs). If you will put the custom configuration files manually, make sure to remove the `aux_file_definitions` variable.

```yaml
# Disable ACME / Let's Encrypt support.
traefik_config_certificatesResolvers_acme_enabled: false

# Disabling ACME support (above) automatically disables the SSL directory to be created.
# Force-enable it to be created with this configuration, because we'll add our certificate files there.
traefik_ssl_dir_enabled: true

# Tell Traefik to load our custom SSL key pair by extending provider configuration.
# The key pair files are created below, in `aux_file_definitions`.
# Note that the `/ssl/…` path is an **in-container path**, not a path on the host (like `/matrix/traefik/ssl`). Do not change it!
traefik_provider_configuration_extension_yaml:
  tls:
    certificates:
      - certFile: /ssl/cert.pem
        keyFile: /ssl/privkey.pem
    stores:
      default:
        defaultCertificate:
          certFile: /ssl/cert.pem
          keyFile: /ssl/privkey.pem

# Use the aux role to create our custom files on the server.
# If you'd like to do this manually, remove this `aux_file_definitions` variable.
aux_file_definitions:
  # Create the privkey.pem file on the server by
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ traefik_ssl_dir_path }}/privkey.pem"
    src: /path/on/your/Ansible/computer/to/privkey.pem
    # Alternatively, comment out `src` above and uncomment the lines below to provide the certificate content inline.
    # Mind the indentation level (indented with two white space characters).
    # content: |
    #   FILE CONTENT
    #   HERE

  # Create the cert.pem file on the server
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ traefik_ssl_dir_path }}/cert.pem"
    src: /path/on/your/Ansible/computer/to/cert.pem
    # Alternatively, comment out `src` above and uncomment the lines below to provide the certificate content inline.
    # Mind the indentation level (indented with two white space characters).
    # content: |
    #   FILE CONTENT
    #   HERE
```

## Use a DNS-01 ACME challenge type, instead of HTTP-01

You can configure Traefik to use the [DNS-01 challenge type](https://letsencrypt.org/docs/challenge-types/#dns-01-challenge) for Let's Encrypt. This is less commonly used than the default [HTTP-01 challenge type](https://letsencrypt.org/docs/challenge-types/#http-01-challenge), but can be helpful to:

- hide your public IP from Let's Encrypt logs
- allow you to obtain SSL certificates for servers which are not accessible (via HTTP) from the public internet (and for which the HTTP-01 challenge would fail)

### Example: Cloudflare

Here is an example for configurations on the `vars.yml` file for Cloudflare. Please adjust it as necessary before applying it.

```yaml
traefik_config_certificatesResolvers_acme_dnsChallenge_enabled: true
traefik_config_certificatesResolvers_acme_dnsChallenge_provider: "cloudflare"
traefik_config_certificatesResolvers_acme_dnsChallenge_delayBeforeCheck: 60
traefik_config_certificatesResolvers_acme_dnsChallenge_resolvers:
  - "1.1.1.1:53"
traefik_environment_variables: |
  CF_API_EMAIL=redacted
  CF_ZONE_API_TOKEN=redacted
  CF_DNS_API_TOKEN=redacted
  LEGO_DISABLE_CNAME_SUPPORT=true
```

Make sure to change the value of "provider" to your particular DNS solution, and provide the appropriate environment variables. The full list of supported providers is available [here](https://doc.traefik.io/traefik/https/acme/#providers).

This example assumes you're using Cloudflare to manage your DNS zone. Note that it requires the use of two tokens: one for reading all zones (`CF_ZONE_API_TOKEN`) and another that must be able to edit the particular domain you're using (`CF_DNS_API_TOKEN`). For security, it's recommended that you create two fine-grained tokens for this purpose, but you might choose to use the same token for both.
