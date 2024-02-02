# Configure Traefik (optional, advanced)

By default, this playbook installs and manages a [Traefik](https://doc.traefik.io/traefik/) reverse-proxy server, powered by the [com.devture.ansible.role.traefik](https://github.com/devture/com.devture.ansible.role.traefik) Ansible role.

This Ansible role support various configuration options. Feel free to consult its `default/main.yml` variables file.


## Adjusting SSL certificate retrieval

See the dedicated [Adjusting SSL certificate retrieval](configuring-playbook-ssl-certificates.md) documentation page.

## Increase logging verbosity

```yaml
devture_traefik_config_log_level: DEBUG
```

## Disable access logs

This will disable access logging.

```yaml
devture_traefik_config_accessLog_enabled: false
```

## Enable Traefik Dashboard

This will enable a Traefik [Dashboard](https://doc.traefik.io/traefik/operations/dashboard/) UI at `https://matrix.DOMAIN/dashboard/` (note the trailing `/`).

```yaml
devture_traefik_dashboard_enabled: true
devture_traefik_dashboard_hostname: "{{ matrix_server_fqn_matrix }}"
devture_traefik_dashboard_basicauth_enabled: true
devture_traefik_dashboard_basicauth_user: YOUR_USERNAME_HERE
devture_traefik_dashboard_basicauth_password: YOUR_PASSWORD_HERE
```

**WARNING**: Enabling the dashboard on a hostname you use for something else (like `matrix_server_fqn_matrix` in the configuration above) may cause conflicts. Enabling the Traefik Dashboard makes Traefik capture all `/dashboard` and `/api` requests and forward them to itself. If any of the services hosted on the same hostname requires any of these 2 URL prefixes, you will experience problems. So far, we're not aware of any playbook services which occupy these endpoints and are likely to cause conflicts.

## Additional configuration

Use the `devture_traefik_configuration_extension_yaml` variable provided by the Traefik Ansible role to override or inject additional settings, even when no dedicated variable exists.

```yaml
# This is a contrived example.
# You can enable and secure the Dashboard using dedicated variables. See above.
devture_traefik_configuration_extension_yaml: |
  api:
    dashboard: true
```

## Reverse-proxying another service behind Traefik

The preferred way to reverse-proxy additional services behind Traefik would be to start the service as another container, configure the container with the corresponding Traefik [container labels](https://docs.docker.com/config/labels-custom-metadata/) (see [Traefik & Docker](https://doc.traefik.io/traefik/routing/providers/docker/)), and connect the service to the `traefik` network. Some services are also already available via the compatible [mash-playbook](https://github.com/mother-of-all-self-hosting/mash-playbook), but take a look at the minor [interoperability adjustments](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/interoperability.md).

However, if your service does not run on a container or runs on another machine, the following configuration might be what you are looking for.

## Reverse-proxying a remote HTTP/HTTPS service behind Traefik

If you want to host another webserver would be reachable via `my-fancy-website.mydomain.com` from the internet and via `https://<internal webserver IP address>:<internal port>` from inside your network, you can make the playbook's integrated Traefik instance reverse-proxy the traffic to the correct host.

Prerequisites: DNS and routing for the domain `my-fancy-website.mydomain.com` need to be set up correctly. In this case, you'd be pointing the domain name to your Matrix server - `my-fancy-website.mydomain.com` would be a CNAME going to `matrix.example.com`.

First, we have to adjust the static configuration of Traefik, so that we can add additional configuration files:

```yaml
# We enable all config files in the /config/ folder to be loaded.
# `/config` is the path as it appears in the Traefik container.
# On the host, it's actually `/matrix/traefik/config` (as defined in `devture_traefik_config_dir_path`).
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      directory: /config/
      watch: true
      filename: ""
```

If you are using a self-signed certificate on your webserver, you can tell Traefik to trust your own backend servers by adding more configuration to the static configuration file. If you do so, bear in mind the security implications of disabling the certificate validity checks towards your back end.

```yaml
# We enable all config files in the /config/ folder to be loaded and
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      directory: /config/
      watch: true
      filename: ""
  serversTransport:
    insecureSkipVerify: true
```


Next, you have to add a new dynamic configuration file for Traefik that contains the actual information of the server using the `aux_file_definitions` variable. In this example, we will terminate SSL at the Traefik instance and connect to the other server via HTTPS. Traefik will now take care of managing the certificates. 

```yaml
aux_file_definitions:
  - dest: "{{ devture_traefik_config_dir_path }}/provider_my_fancy_website.yml"
    content: |
      http:
        routers:
          webserver-router:
            rule: Host(`my_fancy_website.mydomain.com`)
            service: webserver-service
            tls:
              certResolver: default
        services:
          webserver-service:
            loadBalancer:
              servers:
                - url: "https://<internal webserver IP address>:<internal port>"
```
Changing the `url` to one with an `http://` prefix would allow to connect to the server via HTTP.

## Reverse-proxying another service behind Traefik without terminating SSL

If you do not want to terminate SSL at the Traefik instance (for example, because you're already terminating SSL at other webserver), you need to adjust the static configuration in the same way as in the previous chapter in order to be able to add our own dynamic configuration files. Afterwards, you can add the following configuration to your `vars.yml` configuration file:

```yaml
aux_file_definitions:
  - dest: "{{ devture_traefik_config_dir_path }}/providers_my_fancy_website.yml"
    content: |
      tcp:
        routers:
          webserver-router:
            rule: Host(`my_fancy_website.mydomain.com`)
            service: webserver-service
            tls:
              passthrough: true
        services:
          webserver-service:
            loadBalancer:
              servers:
                - url: "https://<internal webserver IP address>:<internal port>"
```
Changing the `url` to one with an `http://` prefix would allow to connect to the server via HTTP.

With these changes, all TCP traffic will be reverse-proxied to the target system. 

**WARNING**: This configuration might lead to problems or need additional steps when a [certbot](https://certbot.eff.org/) behind Traefik also tries to manage [Let's Encrypt](https://letsencrypt.org/) certificates, as Traefik captures all traffic to ```PathPrefix(`/.well-known/acme-challenge/`)```. 


## Traefik behind a `proxy_protocol` reverse-proxy

If you run a reverse-proxy which speaks `proxy_protocol`, add the following to your configuration file:

```yaml
devture_traefik_configuration_extension_yaml: |
  entryPoints:
    web-secure:
      proxyProtocol:
        trustedIPs:
          - "127.0.0.1/32"
          - "<proxy internal IPv4>/32"
          - "<proxy IPv6>/128"
    matrix-federation:
        proxyProtocol:
          trustedIPs:
            - "127.0.0.1/32"
            - "<proxy internal IPv4>/32"
            - "<proxy IPv6>/128"
```
