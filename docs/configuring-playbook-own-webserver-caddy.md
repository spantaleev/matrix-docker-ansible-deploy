
# Using existing Caddy webserver

If you have a server with a Caddy container already serving several applications. And you want to install Matrix on it, but  you don't want to break the existing traffic routing (so that the existing applications keep running smoothly). Then this guide is for you.

## Step 1: Config the playbook-managed-traefik

Use configuration like this (as seen in `examples/vars.yml`):

```yaml
##################################### Using your own webserver ###############################################

matrix_playbook_reverse_proxy_type: playbook-managed-traefik

devture_traefik_config_entrypoint_web_secure_enabled: false

devture_traefik_container_web_host_bind_port: '127.0.0.1:81'

devture_traefik_config_entrypoint_web_forwardedHeaders_insecure: true

matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port: '127.0.0.1:8449'

```

## Step 2: Config caddy container to cooperate with the playbook-managed-traefik container

Firstly, modify the `docker-compose.yaml` file of caddy's.

```yaml

version: "3.9"

services:
  caddy:
    image: caddy:2.5.1-alpine
    networks:
      # add this, so that caddy can talk to the playbook-managed-traefik 
      - traefik
    ports:
      - "80:80"
      - "443:443"
      - "8448:8448"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
    #   - ./site:/var/www
    # other configurations ...

networks:
  # add this as well
  traefik:
    name: traefik
    external: true

```

Then config Caddy webserver container to proxy relevant traffic to the playbook-managed-traefik. 

Copy the content in  `examples/reverse-proxies/caddy2/Caddyfile`, replace localhost and 127.0.0.1 with the relevant docker service name.

```
matrix.example.tld, element.example.tld, etherpadexample.tld, jitsi.example.tld, ntfy.example.tld {

    handle {
        encode zstd gzip

        # reverse_proxy localhost:81  {        
        reverse_proxy matrix-traefik:8080 {  #   <-  Use the service name here.
            header_up X-Forwarded-Port {http.request.port}
            # Other configuration ...
        }
    }
}

# matrix.example.tld:8448 {
https://matrix.example.tld:8448 {   #  <- Enforce https  protocol
    handle {
        encode zstd gzip

        # reverse_proxy 127.0.0.1:8449 {
        reverse_proxy matrix-traefik:8448 {  #  <- Use the service name here.       
            header_up X-Forwarded-Port {http.request.port}
            # Other configurations ...
        }
    }
}

# Other configurations ...

```

