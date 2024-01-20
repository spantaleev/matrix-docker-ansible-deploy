# Nginx Proxy Manager fronting the playbook's integrated Traefik reverse-proxy

Similar to standard nginx, [Nginx Proxy Manager](https://nginxproxymanager.com/) provides nginx capabilities but inside a pre-built Docker container. With the ability for managing proxy hosts and automatic SSL certificates via a simple web interface.

This page summarizes how to use Nginx Proxy Manager (NPM) to front the integrated [Traefik](https://traefik.io/) reverse-proxy webserver.


## Prerequisite configuration

To get started, first follow the [front the integrated reverse-proxy webserver with another reverse-proxy](../../../docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) instructions and update your playbook's configuration (`inventory/host_vars/matrix.<your-domain>/vars.yml`).

If Matrix federation is enabled, then you will need to make changes to [NPM's Docker configuration](https://nginxproxymanager.com/guide/#quick-setup). By default NPM already exposes ports `80` and `443`, but you would also need to **additionally expose the Matrix Federation port** (as it appears on the public side): `8448`.


## Using Nginx Proxy Manager

You'll need to create two proxy hosts in NPM for matrix web and federation traffic.

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
