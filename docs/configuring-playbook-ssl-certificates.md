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
