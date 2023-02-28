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

To use self-signed SSL certificates, you need to disable the certResolvers and the traefik-certs-dumper tool. 
You also need to override the providers.file setting in the Traefik configs. 

Create a file 'certificates.yml' in /devture-traefik/config/ with the following content:

```yaml
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

Place the key and your certificate in /devture-traefik/ssl/

You can use the matrix-aux role for this:

```yaml
matrix_aux_file_definitions:
 - dest: /devture-traefik/ssl/privkey.pem
   src: /path/to/privkey.pem
 - dest: /devture-traefik/ssl/cert.pem
   src: /path/to/cert.pem
 - dest: /devture-traefik/config/certificates.yml
   src: /path/to/certificates.yml
```

Then add the following to your vars.yml:

```yaml
devture_traefik_config_certificatesResolvers_acme_enabled: false
devture_traefik_certResolver_primary: ''
devture_traefik_ssl_dir_enabled: true
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      filename: /config/certificates.yml
      watch: true
matrix_playbook_traefik_certs_dumper_role_enabled: false
```
