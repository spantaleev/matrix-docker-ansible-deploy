# Using your own webserver, instead of this playbook's nginx proxy (optional, advanced)

By default, this playbook installs its own nginx webserver (in a Docker container) which listens on ports 80 and 443.
If that's alright, you can skip this.

If you don't want this playbook's nginx webserver to take over your server's 80/443 ports like that,
and you'd like to use your own webserver (be it nginx, Apache, Varnish Cache, etc.), you can.

All it takes is:

1) making sure your web server user (something like `http`, `apache`, `www-data`, `nginx`) is part of the `matrix` group. You should run something like this: `usermod -a -G matrix nginx`

2) editing your configuration file (`inventory/matrix.<your-domain>/vars.yml`):

```yaml
matrix_nginx_proxy_enabled: false
```

**Note**: even if you do this, in order [to install](installing.md), this playbook still expects port 80 to be available. **Please manually stop your other webserver while installing**. You can start it back again afterwards.

**If your own webserver is nginx**, you can most likely directly use the config files installed by this playbook at: `/matrix/nginx-proxy/conf.d`. Just include them in your `nginx.conf` like this: `include /matrix/nginx-proxy/conf.d/*.conf;`

**If your own webserver is not nginx**, you can still take a look at the sample files in `/matrix/nginx-proxy/conf.d`, and:

- ensure you set up (separate) vhosts that proxy for both Riot (`localhost:8765`) and Matrix Synapse (`localhost:8008`)

- ensure that the `/.well-known/acme-challenge` location for each "port=80 vhost" gets proxied to `http://localhost:2402` (controlled by `matrix_ssl_lets_encrypt_certbot_standalone_http_port`) for automated SSL renewal to work

- ensure that you restart/reload your webserver once in a while, so that renewed SSL certificates would take effect (once a month should be enough)
