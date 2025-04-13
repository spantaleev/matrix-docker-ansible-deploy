<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Ed Geraghty

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring the Traefik reverse-proxy (optional, advanced)

By default, this playbook installs and manages a [Traefik](https://doc.traefik.io/traefik/) reverse-proxy server, powered by the [ansible-role-traefik](https://github.com/mother-of-all-self-hosting/ansible-role-traefik) Ansible role for you. If that's okay, you can skip this document.

## Adjusting the playbook configuration

This Ansible role support various configuration options. Feel free to consult its `default/main.yml` variables file.

### Disable access logs

To disable access logging, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
traefik_config_accessLog_enabled: false
```

### Enable Traefik Dashboard

To enable a Traefik [Dashboard](https://doc.traefik.io/traefik/operations/dashboard/) UI at `https://matrix.example.com/dashboard/` (note the trailing `/`), add the following configuration to your `vars.yml` file:

```yaml
traefik_dashboard_enabled: true
traefik_dashboard_hostname: "{{ matrix_server_fqn_matrix }}"
traefik_dashboard_basicauth_enabled: true
traefik_dashboard_basicauth_user: YOUR_USERNAME_HERE
traefik_dashboard_basicauth_password: YOUR_PASSWORD_HERE
```

> [!WARNING]
> Enabling the dashboard on a hostname you use for something else (like `matrix_server_fqn_matrix` in the configuration above) may cause conflicts. Enabling the Traefik Dashboard makes Traefik capture all `/dashboard` and `/api` requests and forward them to itself. If any of the services hosted on the same hostname requires any of these 2 URL prefixes, you will experience problems. So far, we're not aware of any playbook services which occupy these endpoints and are likely to cause conflicts.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [Traefik role](https://github.com/mother-of-all-self-hosting/ansible-role-traefik)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-traefik/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `traefik_configuration_extension_yaml` variable

For example, to enable and secure the Dashboard, you can add the following configuration to your `vars.yml` file:

**Note**: this is a contrived example as you can enable and secure the Dashboard using the dedicated variables. See above for details.

```yaml
traefik_configuration_extension_yaml: |
  # Your custom YAML configuration for Traefik goes here.
  # This configuration extends the default starting configuration (`traefik_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `traefik_configuration_yaml`.
  #
  # Example configuration extension follows:
  #
  api:
    dashboard: true
```

### Reverse-proxying another service behind Traefik

The preferred way to reverse-proxy additional services behind Traefik would be to start the service as another container, configure the container with the corresponding Traefik [container labels](https://docs.docker.com/config/labels-custom-metadata/) (see [Traefik & Docker](https://doc.traefik.io/traefik/routing/providers/docker/)), and connect the service to the `traefik` network. Some services are also already available via the compatible [mash-playbook](https://github.com/mother-of-all-self-hosting/mash-playbook), but take a look at the minor [interoperability adjustments](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/interoperability.md).

However, if your service does not run on a container or runs on another machine, the following configuration might be what you are looking for.

#### Reverse-proxying a remote HTTP/HTTPS service behind Traefik

If you want to host another webserver would be reachable via `my-fancy-website.example.net` from the internet and via `https://<internal webserver IP address>:<internal port>` from inside your network, you can make the playbook's integrated Traefik instance reverse-proxy the traffic to the correct host.

Prerequisites: DNS and routing for the domain `my-fancy-website.example.net` need to be set up correctly. In this case, you'd be pointing the domain name to your Matrix server — `my-fancy-website.example.net` would be a CNAME going to `matrix.example.com`.

First, we have to adjust the static configuration of Traefik, so that we can add additional configuration files:

```yaml
# We enable all config files in the /config/ folder to be loaded.
# `/config` is the path as it appears in the Traefik container.
# On the host, it's actually `/matrix/traefik/config` (as defined in `traefik_config_dir_path`).
traefik_configuration_extension_yaml: |
  providers:
    file:
      directory: /config/
      watch: true
      filename: ""
```

If you are using a self-signed certificate on your webserver, you can tell Traefik to trust your own backend servers by adding more configuration to the static configuration file. If you do so, bear in mind the security implications of disabling the certificate validity checks towards your back end.

```yaml
# We enable all config files in the /config/ folder to be loaded and
traefik_configuration_extension_yaml: |
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
  - dest: "{{ traefik_config_dir_path }}/provider_my_fancy_website.yml"
    content: |
      http:
        routers:
          webserver-router:
            rule: Host(`my-fancy-website.example.net`)
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

#### Reverse-proxying another service behind Traefik without terminating SSL

If you do not want to terminate SSL at the Traefik instance (for example, because you're already terminating SSL at other webserver), you need to adjust the static configuration in the same way as in the previous chapter in order to be able to add our own dynamic configuration files. Afterwards, you can add the following configuration to your `vars.yml` configuration file:

```yaml
aux_file_definitions:
  - dest: "{{ traefik_config_dir_path }}/providers_my_fancy_website.yml"
    content: |
      tcp:
        routers:
          webserver-router:
            rule: Host(`my-fancy-website.example.net`)
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

> [!WARNING]
> This configuration might lead to problems or need additional steps when a [certbot](https://certbot.eff.org/) behind Traefik also tries to manage [Let's Encrypt](https://letsencrypt.org/) certificates, as Traefik captures all traffic to ```PathPrefix(`/.well-known/acme-challenge/`)```.

#### Traefik behind a `proxy_protocol` reverse-proxy

If you run a reverse-proxy which speaks `proxy_protocol`, add the following configuration to your `vars.yml` file:

```yaml
traefik_configuration_extension_yaml: |
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

## Other configurations

### Adjusting SSL certificate retrieval

See the dedicated [Adjusting SSL certificate retrieval](configuring-playbook-ssl-certificates.md) documentation page.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-traefik`.

### Increase logging verbosity

The default logging level for this component is `INFO`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
traefik_config_log_level: DEBUG
```
