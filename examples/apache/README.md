# Apache reverse-proxy

This directory contains sample files that show you how to do reverse-proxying using Apache.

This is for when you wish to have your own Apache webserver sitting in front of Matrix services installed by this playbook.
See the [Using your own webserver, instead of this playbook's nginx proxy](../../docs/configuring-playbook-own-webserver.md) documentation page.

To use your own Apache reverse-proxy, you first need to disable the integrated nginx server.
You do that with the following custom configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_nginx_proxy_enabled: false
```

You can then use the configuration files from this directory as an example for how to configure your Apache server.

**NOTE**: this is just an example and may not be entirely accurate. It may also not cover other use cases (enabling various services or bridges requires additional reverse-proxying configuration).
