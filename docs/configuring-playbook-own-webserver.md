# Using your own webserver, instead of this playbook's nginx proxy (optional, advanced)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.

If you don't want this playbook's nginx webserver to take over your server's 80/443 ports like that,
and you'd like to use your own webserver (be it nginx, Apache, Varnish Cache, etc.), you can.


## Preparation

No matter which external webserver you decide to go with, you'll need to:

1) Make sure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`

2) Edit your configuration file (`inventory/matrix.<your-domain>/vars.yml`) to disable the integrated nginx server:

```yaml
matrix_nginx_proxy_enabled: false
```

3) **If you'll manage SSL certificates by yourself**, edit your configuration file (`inventory/matrix.<your-domain>/vars.yml`) to disable SSL certificate retrieval:

```yaml
matrix_ssl_retrieval_method: none
```

**Note**: During [installation](installing.md), unless you've disabled SSL certificate management (`matrix_ssl_retrieval_method: none`), the playbook would need 80 to be available, in order to retrieve SSL certificates. **Please manually stop your other webserver while installing**. You can start it back up afterwards.


## Using your own external nginx webserver

Once you've followed the [Preparation](#preparation) guide above, it's time to set up your external nginx server.

Even with `matrix_nginx_proxy_enabled: false`, the playbook still generates some helpful files for you in `/matrix/nginx-proxy/conf.d`.
Those configuration files are adapted for use with an external web server (one not running in the container network).

You can most likely directly use the config files installed by this playbook at: `/matrix/nginx-proxy/conf.d`. Just include them in your own `nginx.conf` like this: `include /matrix/nginx-proxy/conf.d/*.conf;`

Note that if your nginx version is old, it might not like our default choice of SSL protocols (particularly the fact that the brand new `TLSv1.3` protocol is enabled). You can override the protocol list by redefining the `matrix_nginx_proxy_ssl_protocols` variable. Example:

```yaml
# Custom protocol list (removing `TLSv1.3`) to suit your nginx version.
matrix_nginx_proxy_ssl_protocols: "TLSv1.1 TLSv1.2"
```


## Using your own external Apache webserver

Once you've followed the [Preparation](#preparation) guide above, you can take a look at the [examples/apache](../examples/apache) directory for a sample configuration.

## Using your own external caddy webserver

After following  the [Preparation](#preparation) guide above, you can take a look at the [examples/caddy](../examples/caddy) directory for a sample configuration.

## Using another external webserver

Feel free to look at the [examples/apache](../examples/apache) directory, or the [template files in the matrix-nginx-proxy role](../roles/matrix-nginx-proxy/templates/conf.d/).
