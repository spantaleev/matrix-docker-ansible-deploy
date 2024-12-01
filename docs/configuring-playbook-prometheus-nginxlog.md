# Enabling metrics and graphs for NginX logs (optional)

It can be useful to have some (visual) insight into [nginx](https://nginx.org/) logs.

This adds [prometheus-nginxlog-exporter](https://github.com/martin-helmich/prometheus-nginxlog-exporter/) to your Matrix deployment.

It will collect access logs from various nginx reverse-proxies which may be used internally (e.g. `matrix-synapse-reverse-proxy-companion`, if Synapse workers are enabled) and will make them available at a Prometheus-compatible `/metrics` endpoint.

**Note**: nginx is only used internally by this Ansible playbook. With Traefik being our default reverse-proxy, collecting nginx metrics is less relevant.

To make use of this, you need to install [Prometheus](./configuring-playbook-prometheus-grafana.md) either via the playbook or externally. When using an external Prometheus, configuration adjustments are necessary - see [Save metrics on an external Prometheus server](#save-metrics-on-an-external-prometheus-server).

If your setup includes [Grafana](./configuring-playbook-prometheus-grafana.md), a dedicated `NGINX PROXY` Grafana dashboard will be created.

## Configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_prometheus_nginxlog_exporter_enabled: true
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Docker Image Compatibility

At the moment of writing only images for `amd64` and `arm64` architectures are available. The playbook currently does not support [self-building](./self-building.md) a container image on other architectures. You can however use a custom-build image by setting:

```yaml
matrix_prometheus_nginxlog_exporter_docker_image_arch_check_enabled: false
matrix_prometheus_nginxlog_exporter_docker_image: path/to/docker/image:tag
```

## Security and privacy

Metrics and resulting graphs can contain a lot of information. NginX logs contain information like IP address, URLs, UserAgents and more. This information can reveal usage patterns and could be considered Personally Identifiable Information (PII). Think about this before enabling (anonymous) access. Please make sure you change the default Grafana password.

## Save metrics on an external Prometheus server

The playbook will automatically integrate the metrics into the [Prometheus](./configuring-playbook-prometheus-grafana.md) server provided with this playbook (if enabled). In such cases, the metrics endpoint is not exposed publicly - it's only available on the container network.

When using an external Prometheus server, you'll need to expose metrics publicly. See [Collecting metrics to an external Prometheus server](./configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server).

You can either use `matrix_prometheus_nginxlog_exporter_metrics_proxying_enabled: true` to expose just this one service, or `matrix_metrics_exposure_enabled: true` to expose all services.

Whichever way you go with, this service will expose its metrics endpoint **without password-protection** at `https://matrix.example.com/metrics/nginxlog` by default.

For password-protection, use (`matrix_metrics_exposure_http_basic_auth_enabled` and `matrix_metrics_exposure_http_basic_auth_users`) or (`matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_enabled` and `matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_users`).
