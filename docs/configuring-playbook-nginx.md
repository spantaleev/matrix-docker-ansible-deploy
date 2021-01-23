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

## Adjusting SSL in your server

You can adjust how the SSL is served by the nginx server using the `matrix_nginx_proxy_ssl_preset` variable. We support a few presets, based on the Mozilla Server Side TLS
Recommended configurations. These presets influence the TLS Protocol, the SSL Cipher Suites and the `ssl_prefer_server_ciphers` variable of nginx.
Possible values are:

- `"modern"` - For Modern clients that support TLS 1.3, with no need for backwards compatibility
- `"intermediate"` (**default**) - Recommended configuration for a general-purpose server
- `"old"` - Services accessed by very old clients or libraries, such as Internet Explorer 8 (Windows XP), Java 6, or OpenSSL 0.9.8

**Be really carefull when setting it to `"modern"`**. This could break comunication with other Matrix servers, limiting your federation posibilities. The
[Federarion tester](https://federationtester.matrix.org/) also won't work.

Besides changing the preset (`matrix_nginx_proxy_ssl_preset`), you can also directly override these 3 variables:

- `matrix_nginx_proxy_ssl_protocols`: for specifying the supported TLS protocols.
- `matrix_nginx_proxy_ssl_prefer_server_ciphers`: for specifying if the server or the client choice when negotiating the cipher. It can set to `on` or `off`.
- `matrix_nginx_proxy_ssl_ciphers`: for specifying the SSL Cipher suites used by nginx.

For more information about these variables, check the `roles/matrix-nginx-proxy/defaults/main.yml` file.

## Synapse + OpenID Connect for Single-Sign-On

If you want to use OpenID Connect as an SSO provider (as per the [Synapse OpenID docs](https://github.com/matrix-org/synapse/blob/develop/docs/openid.md)), you need to use the following configuration (in your `vars.yml` file) to instruct nginx to forward `/_synapse/oidc` to Synapse:

```yaml
matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_oidc_api_enabled: true
```

## Disable Nginx access logs

This will disable the access logging for nginx.

```yaml
matrix_nginx_proxy_access_log_enabled: false
```
