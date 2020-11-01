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

## Using Keycloak OIDC SSO

If you want to use Keycloak OpenId Connect as SSO provider - see [synapse doc](https://github.com/matrix-org/synapse/blob/develop/docs/openid.md) - , you need to enable following variable to instruc nginx to proceed location /_synapse/oidc/callback  

```yaml
matrix_nginx_proxy_proxy_matrix_synapse_oidc_provider_keycloak: true
```

