# Adjusting SSL certificate retrieval (optional, advanced)

By default, this playbook retrieves and auto-renews free SSL certificates from [Let's Encrypt](https://letsencrypt.org/).

Those certificates are used when configuring the nginx reverse proxy installed by this playbook.

If that's alright, you can skip this.


## Using self-signed SSL certificates

For private deployments (not publicly accessible from the internet), you may not be able to use Let's Encrypt certificates.

If self-signed certificates are alright with you, you can ask the playbook to generate such for you with the following configuration:

```yaml
matrix_ssl_retrieval_method: self-signed
```


## Using your own SSL certificates

If you'd like to manage SSL certificates by yourself and have the playbook use your certificate files, you can use the following configuration:

```yaml
matrix_ssl_retrieval_method: manually-managed
```

With such a configuration, the playbook would expect you to drop the SSL certificate files in the directory specified by `matrix_ssl_config_dir_path` (`/matrix/ssl/config` by default) obeying the following hierarchy:

- `<matrix_ssl_config_dir_path>/live/<domain>/fullchain.pem`
- `<matrix_ssl_config_dir_path>/live/<domain>/privkey.pem`

where `<domain>` refers to the domains that you need (usually `matrix.<your-domain>` and `riot.<your-domain>`).


## Not bothering with SSL certificates

If you're [using an external web server](configuring-playbook-own-webserver.md) which is not nginx, or you would otherwise want to manage its certificates without this playbook getting in the way, you can completely disable SSL certificate management with the following configuration:

```yaml
matrix_ssl_retrieval_method: none
```

With such a configuration, no certificates will be retrieved at all. You're free to manage them however you want.
