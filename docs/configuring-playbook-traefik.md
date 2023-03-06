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

**WARNING**: enabling the dashboard on a hostname you use for something else (like `matrix_server_fqn_matrix` in the configuration above) may cause conflicts. Enabling the Traefik Dashboard makes Traefik capture all `/dashboard` and `/api` requests and forward them to itself. If any of the services hosted on the same hostname requires any of these 2 URL prefixes, you will experience problems. So far, we're not aware of any playbook services which occupy these endpoints and are likely to cause conflicts.

## Additional configuration

Use the `devture_traefik_configuration_extension_yaml` variable provided by the Traefik Ansible role to override or inject additional settings, even when no dedicated variable exists.

```yaml
# This is a contrived example.
# You can enable and secure the Dashboard using dedicated variables. See above.
devture_traefik_configuration_extension_yaml: |
  api:
    dashboard: true
```
