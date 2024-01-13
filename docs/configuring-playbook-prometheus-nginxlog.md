# Enabling metrics and graphs for NginX logs (optional)

It can be useful to have some (visual) insight into NignX logs.

This adds [prometheus-nginxlog-exporter](https://github.com/martin-helmich/prometheus-nginxlog-exporter/) to your matrix deployment.
It will provide a prometheus 'metrics' endpoint exposing data from both the `matrix-nginx-proxy` and `matrix-synapse-reverse-proxy-companion` logs and automatically aggregates the data with prometheus.
Optionally it visualizes the data, if [`matrix-grafana`](configuring-playbook-prometheus-grafana.md) is enabled, by means of a dedicated Grafana dashboard named `NGINX PROXY`

You can enable this role by adding the following settings in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_prometheus_nginxlog_exporter_enabled: true
```

x | Prerequisites | Variable | Description
|:--:|:--:|:--:|:--|
**REQUIRED** | `matrix-prometheus`| `prometheus_enabled`|[Prometheus](https://prometheus.io) is a time series database. It holds all the data we're going to talk about.
_Optional_ | [`matrix-grafana`](configuring-playbook-prometheus-grafana.md) | [`grafana_enabled`](configuring-playbook-prometheus-grafana.md)|[Grafana](https://grafana.com) is the visual component. It shows (on the `stats.<your-domain>` subdomain) graphs that we're interested in. When enabled the `NGINX PROXY` dashboard is automatically added.

## Docker Image Compatibility

At the moment of writing only images for `amd64` and `arm64` architectures are available

The playbook currently does not support [self-building](./self-building.md) a container image on other architectures.
You can however use a custom-build image by setting:

```yaml
matrix_prometheus_nginxlog_exporter_docker_image_arch_check_enabled: false
matrix_prometheus_nginxlog_exporter_docker_image: path/to/docker/image:tag
```

## Security and privacy

Metrics and resulting graphs can contain a lot of information. NginX logs contain information like IP address, URLs, UserAgents and more. This information can reveal usage patterns and could be considered Personally Identifiable Information (PII). Think about this before enabling (anonymous) access.
Please make sure you change the default Grafana password.

## Save metrics on an external Prometheus server

The playbook will automatically integrate the metrics into the [Prometheus](./configuring-playbook-prometheus-grafana.md) server provided with this playbook (if enabled). In such cases, the metrics endpoint is not exposed publicly - it's only available on the container network.

When using an external Prometheus server, you'll need to expose metrics publicly. See [Collecting metrics to an external Prometheus server](./configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server).

You can either use `matrix_prometheus_nginxlog_exporter_metrics_proxying_enabled: true` to expose just this one service, or `matrix_metrics_exposure_enabled: true` to expose all services.

Whichever way you go with, this service will expose its metrics endpoint **without password-protection** at `https://matrix.DOMAIN/metrics/nginxlog` by default.

For password-protection, use (`matrix_metrics_exposure_http_basic_auth_enabled` and `matrix_metrics_exposure_http_basic_auth_users`) or (`matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_enabled` and `matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_users`).


