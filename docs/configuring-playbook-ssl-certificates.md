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

Using self-signed certificates with Traefik is a somewhat involved processes, where you need to manually mount the files into the container and adjust the "static" configuration to refer to them.

Feel free to research this approach on your own and improve this guide!
