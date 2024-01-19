# Nginx reverse-proxy fronting the playbook's integrated Traefik reverse-proxy

This directory contains a sample config that shows you how to use the [nginx](https://nginx.org/) webserver to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver with another reverse-proxy.


## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`).


## Using the nginx configuration

Copy the [matrix.conf](matrix.conf) file to your nginx server's filesystem, modify it to your needs and include it in your nginx configuration (e.g. `include /path/to/matrix.conf;`).

This configuration **disables SSL certificate retrieval**, so you will **need to obtain SSL certificates manually** (e.g. by using [certbot](https://certbot.eff.org/)) and set the appropriate path in `matrix.conf`. In the example nginx configuration, a single certificate is used for all subdomains (`matrix.DOMAIN`, `element.DOMAIN`, etc.). For your setup, may wish to change this and use separate `server` blocks and separate certificate files for each host.

Also note that your copy of the `matrix.conf` file has to be adapted to whatever services you are using. For example, remove `element.domain.com` from the `server_name` list if you don't use [Element](../../../docs/configuring-playbook-client-element.md) web client or add `dimension.domain.com` to it if you do use the [Dimension](../../../docs/configuring-playbook-dimension.md) integration manager.

## Using Nginx Proxy Manager

Similar to standard nginx, [Nginx Proxy Manager](https://nginxproxymanager.com/) provides nginx capabilities but inside a pre-built Docker container. With the ability for managing proxy hosts and automatic SSL certificates via a simple web interface.

If Matrix federation is enabled, then you will need to make changes to [NPM's Docker configuration](https://nginxproxymanager.com/guide/#quick-setup). By default NPM has access to ports 443, 80 and 81, but you would also need to **provide access to the fedderation ports** `8448` and `8449`.


### Creating proxy hosts in Nginx Proxy Manager

Open the 'Proxy Hosts' page in the NPM web interface and select `Add Proxy Host`, the first being for matrix web traffic. Apply the proxys configuration like this:

```md
# Details
# Matrix web proxy config
Domain Names: matrix.DOMAIN
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 81

# Custom locations
# Add one custom location
Define location: /
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 81
Custom config:
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;
    client_max_body_size 50M;

# SSL
# Either 'Request a new certificate' or select an existing one
SSL Certificate: matrix.DOMAIN or *.DOMAIN
Force SSL: true
HTTP/2 Support: true
```

Again, under the 'Proxy Hosts' page select `Add Proxy Host`, this time for your federation traffic. Apply the proxys configuration like this:

```md
# Details
# Matrix Federation proxy config
Domain Names: matrix.DOMAIN:8448
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 8449

# Custom locations
# Add one custom location
Define location: /
Scheme: http
Forward Hostname/IP: IP-ADDRESS-OF-YOUR-MATRIX
Forward Port: 8449
Custom config:
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 50M;

# SSL
# Either 'Request a new certificate' or select an existing one
SSL Certificate: matrix.DOMAIN or *.DOMAIN
Force SSL: true
HTTP/2 Support: true

# Advanced
# Allows NPM to listen on the federation port
Custom Nginx Configuration: listen 8448 ssl http2;
```

Also note, NPM would need to be configured for whatever other services you are using. For example, you would need to create additional proxy hosts for `element.DOMAIN` or `jitsi.DOMAIN`, which would use the forwarding port `81`.
