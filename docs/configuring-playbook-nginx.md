# Configure Nginx (optional, advanced)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.


## Using Nginx status

This will serve a statuspage to the hosting machine only. Useful for monitoring software like [longview](https://www.linode.com/docs/platform/longview/longview-app-for-nginx/)

```yaml
matrix_nginx_proxy_proxy_matrix_nginx_status_enabled: true
```

This will serve the status page under the following addresses:
- `http://matrix.DOMAIN/nginx_status` (using HTTP)
- `https://matrix.DOMAIN/nginx_status` (using HTTPS)

By default, if ```matrix_nginx_proxy_nginx_status_enabled``` is enabled, access to the status page would be allowed from the local IP address of the server. If you wish to allow access from other IP addresses, you can provide them as a list:

```yaml
matrix_nginx_proxy_proxy_matrix_nginx_status_allowed_addresses:
- 8.8.8.8
- 1.1.1.1
```


## Synapse + OpenID Connect for Single-Sign-On

If you want to use OpenID Connect as an SSO provider (as per the [Synapse OpenID docs](https://github.com/matrix-org/synapse/blob/develop/docs/openid.md)), you need to use the following configuration (in your `vars.yml` file) to instruct nginx to forward `/_synapse/oidc` to Synapse:

```yaml
matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_oidc_api_enabled: true
```
