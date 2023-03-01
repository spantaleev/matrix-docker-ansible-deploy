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

To use self-signed SSL certificates, you need to:

- disable `certResolvers` in Traefik, so it won't attempt to retrieve SSL certificates using the default certificate resolver (using [ACME](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment) / [Let's Encrypt](https://letsencrypt.org/))
- put a custom Traefik configuration file on the server, with the help of this Ansible playbook (via the `matrix-aux` role) or manually
- register your custom configuration file with Traefik, by adding an extra provider of type [file](https://doc.traefik.io/traefik/providers/file/)
- put the SSL files on the server, with the help of this Ansible playbook (via the `matrix-aux` role) or manually

```yaml
# Disable ACME / Let's Encrypt support
devture_traefik_config_certificatesResolvers_acme_enabled: false

# Unset the default certificate resolver
devture_traefik_certResolver_primary: ''

# Keep the SSL directory normally used for ACME / Let's Encrypt certificates.
# We need to explicitly enable this, because disabling ACME support (above) automatically disables it otherwise.
devture_traefik_ssl_dir_enabled: true

# Tell Traefik to load our custom configuration file (certificates.yml).
# The file is created below. See `matrix_aux_file_definitions`.
# The `/config/..` path is an in-container path, not a path on the host. Do not change it!
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      filename: /config/certificates.yml
      watch: true

# Use the matrix-aux role to create our custom files on the server.
# If you'd like to do this manually, you remove this `matrix_aux_file_definitions` variable.
matrix_aux_file_definitions:
  # Create the privkey.pem file on the server by
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ devture_traefik_ssl_dir_path }}/privkey.pem"
    src: /path/on/your/Ansible/computer/to/privkey.pem

  # Create the cert.pem file on the server
  # uploading a file from the computer where Ansible is running.
  - dest: "{{ devture_traefik_ssl_dir_path }}/cert.pem"
    src: /path/on/your/Ansible/computer/to/cert.pem

  # Create the custom Traefik configuration.
  # The `/ssl/..` paths below are in-container paths, not paths on the host. Do not change them!
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
