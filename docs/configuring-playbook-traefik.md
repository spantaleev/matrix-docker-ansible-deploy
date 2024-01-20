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

The preferred way to reverse-proxy additional services behind Traefik would be to add the service as another container, configure the container with the corresponding traefik labels, and add it to the `traefik` network. Some services are also already available via the compatible [mash-playbook](https://github.com/mother-of-all-self-hosting/mash-playbook), but take a look at the minor [interoperability adjustments](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/interoperability.md).

However, if your service is not available as a docker container or runs on another machine, the following configuration mighht be what you are looking for.

## Reverse-proxying another HTTP/HTTPS service behind Traefik without using docker

If you want to host another webserver that is reachable via `my_fancy_website.mydomain.com` from the internet and via `https://<internal webserver IP address>:<internal port>` from inside your network, you can make traefik reverse-proxy the traffic to the correct host.

Prerequisites: DNS and routing for the domain `my_fancy_website.mydomain.com` need to be set up correctly to reach your traefik instance.

First, we have to adjust the static configuration of traefik, so that we can add additional configuration files:

```yaml
# We enable all config files in the /config/ folder to be loaded.
devture_traefik_configuration_extension_yaml: |
  providers:
    file:
      directory: /config/
      watch: true
      filename: ""
```

If you are using a self signed certificate on your webserver, you can tell traefik to trust your own backend servers by adding more configuration to the static configuration file. If you do so, bear in mind the security implications of disabling the certificate validity checks towards your back end.

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


Next, you have to add a new dynamic configuration file for traefik that contains the actual information of the server using the `aux_file_definitions` variable. In this example, we will terminate SSL at the traefik instance and connect to the other server via HTTPS. Traefik will now take care of managing the certificates. 

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
Changing the url to HTTP would allow to connect to the server via HTTP.

## Reverse-proxying another service behind Traefik without terminating SSL

If you do not want to terminate SSL on the traefik instance, you need to adjust the static configuration in the same way as in the previous chapter in order to be able to add our own dynamic configuration files. Afterwards, you can enter the following configuration to the dynamic configuration file:

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
Changing the url to HTTP would allow to connect to the server via HTTP.

With these changes, all TCP traffic will be reverse-proxied to the target system. 

**WARNING**: This configuration might lead to problems or need additional steps when a certbot behind traefik also tries to manage Let's Encrypt certificates, as traefik captures all traffic to ```PathPrefix(`/.well-known/acme-challenge/`)```. 
