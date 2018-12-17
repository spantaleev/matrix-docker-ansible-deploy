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

- ensure that the `/.well-known/acme-challenge` location for each "port=80 vhost" gets proxied to `http://localhost:2402` (controlled by `matrix_ssl_certbot_standalone_http_port`) for automated SSL renewal to work

- ensure that you restart/reload your webserver once in a while, so that renewed SSL certificates would take effect (once a month should be enough)

**Apache2 sample configuration file**

1. Create a new apache configuration file named 000-matrix-ssl.conf and enable it. Make certain to replace DOMAIN/SSL values with the correct ones for your server.

       # Auto redirect http to https
       <VirtualHost *:80>
           ServerName matrix.DOMAIN
           Redirect permanent / https://matrix.DOMAIN/
       </VirtualHost>

       <VirtualHost *:443>
           ServerName matrix.DOMAIN

           SSLEngine On
           SSLCertificateFile /etc/letsencrypt/live/DOMAIN/fullchain.pem
           SSLCertificateKeyFile /etc/letsencrypt/live/DOMAIN/privkey.pem

           SSLProxyEngine on
           SSLProxyProtocol +TLSv1.1 +TLSv1.2
           SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
            
           ProxyPreserveHost On
           ProxyRequests Off
           ProxyVia On
           # Keep /.well-known/matrix/client and /_matrix/identity free for different proxy/location
           ProxyPassMatch ^/.well-known/matrix/client !
           ProxyPassMatch ^/_matrix/identity !
           # Proxy all 443 traffic to the synapse matrix client api
           ProxyPass / http://localhost:8008/
           ProxyPassReverse / http://localhost:8008/

           # Map /.well-known/matrix/client for client discovery
           Alias /.well-known/matrix/client /matrix/static-files/.well-known/matrix/client
           <Files "/matrix/static-files/.well-known/matrix/client">
               Require all granted
           </Files>
           <Location "/.well-known/matrix/client>
               Header always set Content-Type "application/json"
               Header always set Access-Control-Allow-Origin "*"
           </Location>
           <Directory /matrix/static-files/.well-known/matrix/>
               AllowOverride All
               # Apache 2.4:
               Require all granted
               # Or for Apache 2.2:
               #order allow,deny
           </Directory>
            
           # Map /_matrix/identity to the identity server
           <Location /_matrix/identity>
               ProxyPass http://localhost:8090/_matrix/identity
           </Location>

           ErrorLog ${APACHE_LOG_DIR}/synapse-error.log
           CustomLog ${APACHE_LOG_DIR}/synapse-access.log combined
       </VirtualHost>

2. Enable required apache2 modules

       a2enmod proxy
       a2enmod proxy_http
       a2enmod proxy_connect
       a2enmod proxy_html
       a2enmod headers
    
3. Reload apache

       systemctl restart apache2

Notes: port 8448 does not get proxied and is left available for the homeserver federation api.
