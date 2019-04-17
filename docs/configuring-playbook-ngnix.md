# Configure Ngnix (optional, advanced)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.


## Using Ngnix status

This will serve a statuspage to the hosting machine only. Useful for monitoring software like [longview](https://www.linode.com/docs/platform/longview/longview-app-for-nginx/)

```yaml
matrix_nginx_proxy_nginx_status_enabled: true
```
